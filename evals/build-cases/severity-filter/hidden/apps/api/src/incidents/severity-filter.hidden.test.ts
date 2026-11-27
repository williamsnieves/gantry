import type { Request, Response, Router } from "express";
import { describe, expect, it, vi } from "vitest";
import type { Actor } from "./incident";
import type { IncidentRepository } from "./incident-repository";
import { registerIncidentRoutes } from "./incidents-controller";
import { PrismaIncidentRepository } from "./prisma-incident-repository";
import type { UpdateIncidentSeverity } from "./update-incident-severity";

function repository() {
  const findMany = vi.fn().mockResolvedValue([]);
  return { findMany, incidents: new PrismaIncidentRepository({ incident: { findMany } } as never) };
}
const whereOf = (findMany: ReturnType<typeof vi.fn>) => findMany.mock.calls[0][0].where;

describe("PrismaIncidentRepository.listByTenant (hidden)", () => {
  it("lists the tenant's incidents when no filter is given", async () => {
    const { findMany, incidents } = repository();
    await incidents.listByTenant("t1");
    expect(whereOf(findMany).tenantId).toBe("t1");
    expect(whereOf(findMany).severity).toBeUndefined();
  });

  it("narrows by severity", async () => {
    const { findMany, incidents } = repository();
    await incidents.listByTenant("t1", { severity: "SEV1" });
    expect(whereOf(findMany).severity).toBe("SEV1");
  });

  it("[edge] keeps the tenant condition when a severity is given", async () => {
    const { findMany, incidents } = repository();
    await incidents.listByTenant("t1", { severity: "SEV1" });
    expect(whereOf(findMany).tenantId).toBe("t1");
  });
});

type Handler = (req: Request, res: Response) => Promise<void>;
const actor: Actor = { userId: "u1", tenantId: "t1", role: "responder", isSupport: false };

async function list(query: Record<string, unknown>) {
  const handlers = new Map<string, Handler>();
  const router = new Proxy({}, { get: (_target, method: string) => (path: string, handler: Handler) => handlers.set(`${method.toUpperCase()} ${path}`, handler) }) as unknown as Router;
  const listByTenant = vi.fn().mockResolvedValue([]);
  registerIncidentRoutes(router, { listByTenant } as unknown as IncidentRepository, {} as UpdateIncidentSeverity);
  const res = { status: vi.fn().mockReturnThis(), json: vi.fn() };
  await handlers.get("GET /incidents")!({ actor, query } as unknown as Request, res as unknown as Response);
  return { res, listByTenant };
}

describe("GET /incidents (hidden)", () => {
  it("lists the actor's tenant without a severity when none is sent", async () => {
    const { res, listByTenant } = await list({});
    expect(listByTenant.mock.calls[0][0]).toBe("t1");
    expect(listByTenant.mock.calls[0][1]?.severity).toBeUndefined();
    expect(res.json).toHaveBeenCalledWith([]);
  });

  it("passes a valid severity to the repository", async () => {
    const { listByTenant } = await list({ severity: "SEV2" });
    expect(listByTenant).toHaveBeenCalledWith("t1", { severity: "SEV2" });
  });

  it("rejects an unknown severity with 400 and does not query", async () => {
    const { res, listByTenant } = await list({ severity: "bogus" });
    expect(res.status).toHaveBeenCalledWith(400);
    expect(res.json).toHaveBeenCalledWith({ error: "invalid_severity" });
    expect(listByTenant).not.toHaveBeenCalled();
  });

  it("[edge] rejects a repeated severity parameter with 400 and does not query", async () => {
    const { res, listByTenant } = await list({ severity: ["SEV1", "SEV2"] });
    expect(res.status).toHaveBeenCalledWith(400);
    expect(listByTenant).not.toHaveBeenCalled();
  });

  it("[edge] rejects a lowercase severity instead of guessing", async () => {
    const { res, listByTenant } = await list({ severity: "sev1" });
    expect(res.status).toHaveBeenCalledWith(400);
    expect(listByTenant).not.toHaveBeenCalled();
  });
});
