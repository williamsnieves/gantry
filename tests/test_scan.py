"""The security scan: rules over the lines a change adds. Run: python3 tests/test_scan.py"""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "distribution/core/.harness/bin"
sys.path.insert(0, str(BIN))
import route  # noqa: E402
import scan  # noqa: E402

# Built from pieces so this file holds nothing a secret scanner would stop.
GITHUB = "gh" + "p_" + "a1B2" * 9
STRIPE = "sk" + "_live_" + "a1B2c3D4" * 3
AWS = "AK" + "IA" + "ABCDEFGHIJKLMNOP"
KEY = "-----BEGIN RSA " + "PRIVATE KEY-----"


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args], cwd=cwd, check=True, capture_output=True)


def run(tool, *args, cwd, expect=0):
    proc = subprocess.run([sys.executable, str(BIN / tool), *args], cwd=cwd, capture_output=True, text=True)
    assert proc.returncode == expect, (args, proc.returncode, proc.stdout, proc.stderr)
    return proc.stdout


# Terraform: what gets deployed. Inbound from anywhere is a finding; outbound to anywhere is how most networks are set.
TERRAFORM = """resource "aws_security_group" "web" {
  ingress {
    from_port   = 22
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "aws_security_group_rule" "admin" {
  cidr_blocks = ["0.0.0.0/0"]
  type        = "ingress"
}
resource "aws_security_group_rule" "out" {
  type        = "egress"
  cidr_blocks = ["0.0.0.0/0"]
}
resource "aws_route" "default" {
  destination_cidr_block = "0.0.0.0/0"
}
resource "google_compute_firewall" "open" {
  source_ranges = ["0.0.0.0/0"]
}
resource "aws_s3_bucket_public_access_block" "assets" {
  block_public_acls = false
}
resource "aws_db_instance" "main" {
  publicly_accessible = true
  storage_encrypted   = false
  # acl = "public-read"
}
data "aws_iam_policy_document" "all" {
  statement {
    actions   = ["*"]
    resources = ["*"]
  }
}
resource "aws_iam_role_policy" "narrow" {
  policy = jsonencode({ Statement = [{ Action = ["s3:GetObject"], Resource = "*" }] })
}
"""
tf = TERRAFORM.splitlines()
infra = {number: found for number in range(1, len(tf) + 1) if (found := scan.infrastructure(tf, number, tf[number - 1]))}
assert infra == {
    4: ["network rule open to any address"], 12: ["network rule open to any address"], 23: ["network rule open to any address"],
    26: ["public storage"], 29: ["database or service reachable from the internet"], 30: ["encryption turned off"],
    35: ["permission for any action or any principal"],
}, infra


with tempfile.TemporaryDirectory() as tmp:
    project = Path(tmp).resolve()
    (project / "src").mkdir()
    # What the project already contained is not the change's doing.
    (project / "src/legacy.ts").write_text(f"const old = eval(input);\nconst token = \"{GITHUB}\";\n")
    (project / "src/app.ts").write_text("export const a = 1;\n")
    git(project, "init", "-q", "-b", "main")
    git(project, "add", "-A")
    git(project, "commit", "-q", "-m", "base")
    git(project, "checkout", "-q", "-b", "feature")

    def found():
        return scan.findings(project, route.change_identity(project)[1], route.base_commit(project))

    (project / "src/app.ts").write_text("export const a = 2;\n")
    (project / "src/legacy.ts").write_text(f"const old = eval(input);\nconst token = \"{GITHUB}\";\nexport {{}};\n")
    assert not any(found().values()), found()
    assert "SECURITY SCAN: PASS (2 changed files)" in run("scan.py", cwd=project)

    # Secrets, in an edited file and in a new one; the value is never printed.
    (project / "src/app.ts").write_text(f"export const a = 2;\nconst stripe = \"{STRIPE}\";\n")
    (project / "deploy.sh").write_text(f"export AWS_ACCESS_KEY_ID={AWS}\n")
    (project / "key.txt").write_text(KEY + "\nabc\n")
    secrets = {(f["what"], f["path"], f["line"]) for f in found()["secret"]}
    assert secrets == {("Stripe live key", "src/app.ts", 2), ("AWS access key", "deploy.sh", 1), ("private key", "key.txt", 1)}, secrets
    out = run("scan.py", cwd=project, expect=1)
    assert "SECURITY SCAN: FAIL" in out and "Stripe live key at src/app.ts:2" in out and STRIPE not in out and AWS not in out, out

    # The final gate blocks on a secret whatever the gates said, and the plan says so up front.
    plan = ("plan", "--runtime", "claude", "--work-mode", "IMPLEMENTATION", "--scope", "BACKEND")
    out = run("route.py", *plan, cwd=project)
    assert "Secret in the change, the final gate will block: Stripe live key at src/app.ts:2" in out, out
    out = run("route.py", "ready", "--runtime", "claude", cwd=project, expect=1)
    assert "the change adds what looks like a secret" in out and "rotate it" in out and STRIPE not in out, out

    # A marked line is an exception a person confirms; possible credentials are conditions, placeholders are not.
    (project / "deploy.sh").unlink()
    (project / "key.txt").unlink()
    (project / "src/app.ts").write_text(
        f"export const a = 2;\nconst fixture = \"{STRIPE}\"; // gantry:allow documented test key\n"
        "const password = \"hunter2hunter2hunter2\";\n"
        "const apiKey = \"your-api-key-here\";\n"
        "const db = \"postgres://app:s3cr3tpass@db.internal:5432/app\";\n"
        "const local = \"postgres://app:app@localhost:5432/app\";\n")
    (project / ".env").write_text("PORT=3000\n")
    (project / ".env.example").write_text("PORT=3000\n")
    result = found()
    assert not result["secret"] and [f["line"] for f in result["allowed"]] == [2], result
    assert {(f["path"], f["line"]) for f in result["suspect"]} == {("src/app.ts", 3), ("src/app.ts", 5), (".env", 0)}, result["suspect"]
    run("route.py", *plan, cwd=project)
    reports = project / ".harness/runtime/claude/artifacts"
    reports.mkdir(parents=True)
    for agent in ("validator", "backend-code-review", "detail-analyst", "reviewer"):
        (reports / f"{agent}-report.md").write_text("ok\n")
        run("route.py", "gate", "--runtime", "claude", "--agent", agent, "--decision", "PASS",
            "--report", f".harness/runtime/claude/artifacts/{agent}-report.md", cwd=project)
    out = run("route.py", "ready", "--runtime", "claude", cwd=project)
    assert out.startswith("PRE_PR_PASS_WITH_CONDITIONS") and "marked `gantry:allow`" in out and "possible credential" in out, out
    (project / ".env").unlink()

    # A risky pattern is a reason for the Security gate to look: it adds the trigger, and can be dismissed with a reason.
    (project / "src/app.ts").write_text(
        "export const a = 2;\n"
        "const rows = await prisma.$queryRawUnsafe(`select * from incidents where id = ${id}`);\n"
        "el.innerHTML = html;\n"
        "const digest = createHash(\"md5\").update(password).digest(\"hex\");\n")
    (project / "notes.md").write_text("Never call eval(input) on user data.\n")
    risky = {(f["what"], f["line"]) for f in found()["risky"]}
    assert risky == {("query built from a string", 2), ("markup injected without escaping", 3), ("weak hash", 4)}, risky
    out = run("route.py", *plan, cwd=project)
    assert "Added from the changed files: SECURITY (the security scan found query built from a string at src/app.ts:2" in out, out
    assert "REQUIRED        security" in out, out
    out = run("route.py", *plan, "--dismiss", "SECURITY=the query has no user input and the hash is a cache key", cwd=project)
    assert "REQUIRED        security" not in out, out
    (project / "src/app.ts").write_text("export const a = 3;\n")
    (project / "notes.md").unlink()
    run("route.py", *plan, "--dismiss", "SECURITY=nothing", cwd=project, expect=2)

# Each risky rule fires on its pattern and stays quiet on the safe form.
FIRES = {
    "dynamic code execution": ["const v = eval(body.code);", "const f = new Function(src);"],
    "markup injected without escaping": ["<div dangerouslySetInnerHTML={{ __html: text }} />", "<p v-html=\"bio\"></p>"],
    "shell command built from a string": ["subprocess.run(cmd, shell=True)", "os.system(command)", "execSync(`rm -rf ${dir}`);"],
    "query built from a string": ["cur.execute(f\"SELECT * FROM users WHERE id = {uid}\")", "db.query(\"select * from t where id = \" + id);"],
    "unsafe deserialization": ["data = pickle.loads(blob)", "cfg = yaml.load(text)"],
    "TLS verification disabled": ["requests.get(url, verify=False)", "new Agent({ rejectUnauthorized: false })"],
    "weak hash": ["hashlib.md5(password.encode())"],
    "any origin allowed": ["res.setHeader(\"Access-Control-Allow-Origin\", \"*\");", "app.use(cors({ origin: \"*\" }));"],
}
QUIET = ["const retrieval = retrieve(x);", "cfg = yaml.load(text, Loader=yaml.SafeLoader)", "requests.get(url, verify=True)",
         "db.query(\"select * from t where id = $1\", [id]);", "execSync(\"npm test\");", "el.textContent = html;",
         "createHash(\"sha256\")", "app.use(cors({ origin: \"https://app.example.com\" }));", "medieval(x)", "model.eval()"]
for name, pattern in scan.RISKY:
    for line in FIRES[name]:
        assert pattern.search(line), (name, line)
    for line in QUIET:
        assert not pattern.search(line), (name, line)

# Performance rules read the lines around the added one: a loop of the same function counts, a loop elsewhere does not.
def slow(code, number=None):
    lines = code.strip("\n").split("\n")
    return [what for n in ([number] if number else range(1, len(lines) + 1)) for what in scan.slow(lines, n)]

LOOPED = [
    "for (const id of ids) {\n  const user = await this.userRepository.findById(id);\n}",
    "const users = await Promise.all(ids.map(async (id) => await prisma.user.findUnique({ where: { id } })));",
    "items.forEach(async (item) => {\n  if (item.stale) {\n    await fetch(item.url);\n  }\n});",
    "for row in rows:\n    owner = session.query(User).get(row.owner_id)",
    "while page:\n    for item in page:\n        requests.post(url, json=item)",
]
NOT_LOOPED = [
    "const user = await this.userRepository.findById(id);",
    "await outboxRepository.markProcessed(events.map((e) => e.id));",                    # the loop builds the argument
    "for (const id of ids) {\n  total += 1;\n}\nconst user = await prisma.user.count();",  # the loop already ended
    "for (const id of ids) {\n  run(async function load() {\n    await fetch(url);\n  });\n}",  # another function's body
    "for row in rows:\n    total += row.amount\nrequests.post(url, json=total)",
    "// for (const id of ids) await prisma.user.findUnique(id)",
]
for code in LOOPED:
    assert "query or request inside a loop" in slow(code), code
for code in NOT_LOOPED:
    assert "query or request inside a loop" not in slow(code), code
UNBOUNDED = ["const rows = await prisma.incident.findMany({ where: { tenantId } });",
             "const rows = await prisma.incident.findMany({\n  where: { tenantId },\n  orderBy: { createdAt: \"desc\" },\n});",
             "const all = await Incident.find({});", "const all = await repo.find();"]
BOUNDED = ["const rows = await prisma.incident.findMany({ where: { tenantId }, take: 50 });",
           "const rows = await prisma.incident.findMany({\n  where: { tenantId },\n  take: limit,\n  cursor,\n});",
           "const all = await Incident.find({}).limit(20);", "const one = items.find((i) => i.id === id);"]
for code in UNBOUNDED:
    assert slow(code, 1) == ["list read without a limit"], code
for code in BOUNDED:
    assert slow(code) == [], code

# In a change: only added lines of runtime code count, and the finding routes the Performance gate until a person dismisses it.
with tempfile.TemporaryDirectory() as tmp:
    project = Path(tmp).resolve()
    (project / "src").mkdir()
    (project / "src/list.ts").write_text("export async function old(ids) {\n  for (const id of ids) {\n    await db.get(id);\n  }\n}\n")
    git(project, "init", "-q", "-b", "main")
    git(project, "add", "-A")
    git(project, "commit", "-q", "-m", "base")
    git(project, "checkout", "-q", "-b", "feature")
    with (project / "src/list.ts").open("a") as file:
        file.write("export const label = 'x';\n")
    (project / "tests").mkdir()
    (project / "tests/list.test.ts").write_text("for (const id of ids) {\n  await db.get(id);\n}\n")
    assert "SECURITY SCAN: PASS" in run("scan.py", cwd=project)  # the old loop and the test are not the change's doing
    (project / "src/owners.ts").write_text("export async function owners(rows) {\n  for (const row of rows) {\n    row.owner = await db.user.get(row.ownerId);\n  }\n}\n")
    out = run("scan.py", cwd=project)
    assert "slow: query or request inside a loop at src/owners.ts:3 (routes the Performance gate)" in out, out
    # Rewriting a line that was already slow adds nothing; a second one in the same file does.
    (project / "src/list.ts").write_text("export async function old(ids) {\n  for (const id of ids) {\n    await db.get(id, { fresh: true });\n  }\n}\n")
    assert "src/list.ts" not in run("scan.py", cwd=project)
    with (project / "src/list.ts").open("a") as file:
        file.write("export async function more(ids) {\n  for (const id of ids) {\n    await db.put(id);\n  }\n}\n")
    assert run("scan.py", cwd=project).count("src/list.ts") == 1
    (project / "src/list.ts").write_text("export async function old(ids) {\n  for (const id of ids) {\n    await db.get(id);\n  }\n}\n")
    plan = ("plan", "--runtime", "claude", "--work-mode", "IMPLEMENTATION", "--scope", "BACKEND")
    out = run("route.py", *plan, cwd=project)
    assert "PERFORMANCE (the scan found query or request inside a loop at src/owners.ts:3" in out and "REQUIRED        performance" in out, out
    out = run("route.py", *plan, "--dismiss", "PERFORMANCE=rows is at most three", cwd=project)
    assert "REQUIRED        performance" not in out, out

    # Terraform in a change: the path routes Infrastructure, a risky setting adds Security, and a state file is never clean.
    (project / "infra").mkdir()
    (project / "infra/main.tf").write_text(TERRAFORM)
    (project / "infra/terraform.tfstate").write_text("{}\n")
    result = found()
    assert {(f["what"], f["line"]) for f in result["risky"] if f["path"] == "infra/main.tf"} >= {
        ("network rule open to any address", 4), ("public storage", 26), ("permission for any action or any principal", 35)}, result["risky"]
    assert ("Terraform state file in the change, which holds secrets in plain text", "infra/terraform.tfstate") in {
        (f["what"], f["path"]) for f in result["suspect"]}, result["suspect"]
    out = run("route.py", *plan, cwd=project)
    assert "network rule open to any address at infra/main.tf:4" in out and "REQUIRED        security" in out and "REQUIRED        infrastructure" in out, out

print("SCAN TESTS: PASS")
