import type { Request, Response, Router } from "express";
import { describe, expect, it, vi } from "vitest";
import type { Actor } from "./incident";
import type { IncidentRepository } from "./incident-repository";
import { registerIncidentRoutes } from "./incidents-controller";
import type { UpdateIncidentSeverity } from "./update-incident-severity";

type Handler = (req: Request, res: Response) => Promise<void>;

const actor: Actor = { userId: "u1", tenantId: "t1", role: "responder", isSupport: false };

function listRoute() {
  const handlers = new Map<string, Handler>();
  const router = {
    get: (path: string, handler: Handler) => handlers.set(`GET ${path}`, handler),
    patch: (path: string, handler: Handler) => handlers.set(`PATCH ${path}`, handler),
  } as unknown as Router;
  const listByTenant = vi.fn().mockResolvedValue([]);
  const incidents = { listByTenant } as unknown as IncidentRepository;
  registerIncidentRoutes(router, incidents, {} as UpdateIncidentSeverity);

  return async (query: Record<string, unknown>) => {
    const res = { status: vi.fn().mockReturnThis(), json: vi.fn() };
    await handlers.get("GET /incidents")!({ actor, query } as unknown as Request, res as unknown as Response);
    return { res, listByTenant };
  };
}

describe("GET /incidents", () => {
  it("lists the actor's tenant without a severity when none is sent", async () => {
    const { res, listByTenant } = await listRoute()({});
    expect(listByTenant).toHaveBeenCalledWith("t1", { severity: undefined });
    expect(res.json).toHaveBeenCalledWith([]);
  });

  it("passes a valid severity to the repository", async () => {
    const { listByTenant } = await listRoute()({ severity: "SEV1" });
    expect(listByTenant).toHaveBeenCalledWith("t1", { severity: "SEV1" });
  });

  it("rejects an unknown severity without querying", async () => {
    const { res, listByTenant } = await listRoute()({ severity: "bogus" });
    expect(res.status).toHaveBeenCalledWith(400);
    expect(res.json).toHaveBeenCalledWith({ error: "invalid_severity" });
    expect(listByTenant).not.toHaveBeenCalled();
  });

  it("still accepts unrelated query parameters", async () => {
    const { listByTenant } = await listRoute()({ page: "2" });
    expect(listByTenant).toHaveBeenCalledWith("t1", { severity: undefined });
  });
});
