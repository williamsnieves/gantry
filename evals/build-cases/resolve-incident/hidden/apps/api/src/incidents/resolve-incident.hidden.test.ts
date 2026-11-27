import type { Request, Response, Router } from "express";
import { describe, expect, it, vi } from "vitest";
import { ForbiddenError, NotFoundError, type Actor, type Incident } from "./incident";
import type { IncidentRepository } from "./incident-repository";
import { registerIncidentRoutes } from "./incidents-controller";
import { ResolveIncident } from "./resolve-incident";
import type { UpdateIncidentSeverity } from "./update-incident-severity";

function repository(rows: Incident[]) {
  const save = vi.fn(async (incident: Incident) => {
    rows.splice(rows.findIndex((row) => row.id === incident.id), 1, incident);
  });
  const incidents = {
    findById: async (id: string) => rows.find((row) => row.id === id) ?? null,
    listByTenant: async (tenantId: string) => rows.filter((row) => row.tenantId === tenantId),
    save,
  } as unknown as IncidentRepository;
  return { incidents, save, rows };
}

const open: Incident = { id: "i1", tenantId: "t1", title: "API down", severity: "SEV2", status: "OPEN" };
const commander: Actor = { userId: "u1", tenantId: "t1", role: "commander", isSupport: false };

describe("ResolveIncident (hidden)", () => {
  it("resolves an open incident and keeps its other fields", async () => {
    const { incidents, rows } = repository([{ ...open }]);
    await new ResolveIncident(incidents).execute(commander, "i1");
    expect(rows[0]).toEqual({ ...open, status: "RESOLVED" });
  });

  it("succeeds on an incident that is already resolved and leaves it resolved", async () => {
    const { incidents, rows } = repository([{ ...open, status: "RESOLVED" }]);
    await expect(new ResolveIncident(incidents).execute(commander, "i1")).resolves.toBeUndefined();
    expect(rows[0].status).toBe("RESOLVED");
  });

  it("reports a missing incident", async () => {
    const { incidents } = repository([]);
    await expect(new ResolveIncident(incidents).execute(commander, "nope")).rejects.toBeInstanceOf(NotFoundError);
  });

  it("reports an incident of another tenant as missing to a commander", async () => {
    const { incidents, save } = repository([{ ...open }]);
    await expect(new ResolveIncident(incidents).execute({ ...commander, tenantId: "t2" }, "i1")).rejects.toBeInstanceOf(NotFoundError);
    expect(save).not.toHaveBeenCalled();
  });

  it("forbids a responder of the same tenant", async () => {
    const { incidents, save } = repository([{ ...open }]);
    await expect(new ResolveIncident(incidents).execute({ ...commander, role: "responder" }, "i1")).rejects.toBeInstanceOf(ForbiddenError);
    expect(save).not.toHaveBeenCalled();
  });

  it("[edge] reports an incident of another tenant as missing to a responder too", async () => {
    const { incidents } = repository([{ ...open }]);
    const outsider: Actor = { ...commander, tenantId: "t2", role: "responder" };
    await expect(new ResolveIncident(incidents).execute(outsider, "i1")).rejects.toBeInstanceOf(NotFoundError);
  });

  it("[edge] forbids a responder even when the incident is already resolved", async () => {
    const { incidents } = repository([{ ...open, status: "RESOLVED" }]);
    await expect(new ResolveIncident(incidents).execute({ ...commander, role: "responder" }, "i1")).rejects.toBeInstanceOf(ForbiddenError);
  });
});

type Handler = (req: Request, res: Response) => Promise<void>;

async function post(execute: ResolveIncident["execute"]) {
  const handlers = new Map<string, Handler>();
  const router = {
    get: (path: string, handler: Handler) => handlers.set(`GET ${path}`, handler),
    patch: (path: string, handler: Handler) => handlers.set(`PATCH ${path}`, handler),
    post: (path: string, handler: Handler) => handlers.set(`POST ${path}`, handler),
  } as unknown as Router;
  registerIncidentRoutes(router, {} as IncidentRepository, {} as UpdateIncidentSeverity, { execute } as unknown as ResolveIncident);
  const res = { status: vi.fn().mockReturnThis(), json: vi.fn(), end: vi.fn(), sendStatus: vi.fn() };
  await handlers.get("POST /incidents/:id/resolve")!({ actor: commander, params: { id: "i1" } } as unknown as Request, res as unknown as Response);
  return res;
}
const statusOf = (res: Awaited<ReturnType<typeof post>>) => res.status.mock.calls[0]?.[0] ?? res.sendStatus.mock.calls[0]?.[0];

describe("POST /incidents/:id/resolve (hidden)", () => {
  it("answers 204 and resolves as the caller", async () => {
    const execute = vi.fn().mockResolvedValue(undefined);
    const res = await post(execute);
    expect(execute).toHaveBeenCalledWith(commander, "i1");
    expect(statusOf(res)).toBe(204);
  });

  it("answers 404 not_found", async () => {
    const res = await post(vi.fn().mockRejectedValue(new NotFoundError("i1")));
    expect(statusOf(res)).toBe(404);
    expect(res.json).toHaveBeenCalledWith({ error: "not_found" });
  });

  it("answers 403 forbidden", async () => {
    const res = await post(vi.fn().mockRejectedValue(new ForbiddenError("no")));
    expect(statusOf(res)).toBe(403);
    expect(res.json).toHaveBeenCalledWith({ error: "forbidden" });
  });
});
