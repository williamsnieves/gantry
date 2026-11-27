import type { Request, Response, Router } from "express";
import { describe, expect, it, vi } from "vitest";
import { ForbiddenError, NotFoundError, type Actor } from "./incident";
import type { IncidentRepository } from "./incident-repository";
import { registerIncidentRoutes } from "./incidents-controller";
import type { ResolveIncident } from "./resolve-incident";
import type { UpdateIncidentSeverity } from "./update-incident-severity";

type Handler = (req: Request, res: Response) => Promise<void>;

const actor: Actor = { userId: "u1", tenantId: "t1", role: "commander", isSupport: false };

function resolveRoute(execute: ResolveIncident["execute"]) {
  const handlers = new Map<string, Handler>();
  const router = {
    get: (path: string, handler: Handler) => handlers.set(`GET ${path}`, handler),
    patch: (path: string, handler: Handler) => handlers.set(`PATCH ${path}`, handler),
    post: (path: string, handler: Handler) => handlers.set(`POST ${path}`, handler),
  } as unknown as Router;
  registerIncidentRoutes(router, {} as IncidentRepository, {} as UpdateIncidentSeverity, { execute } as ResolveIncident);

  return async () => {
    const res = { status: vi.fn().mockReturnThis(), json: vi.fn(), end: vi.fn() };
    await handlers.get("POST /incidents/:id/resolve")!({ actor, params: { id: "i1" } } as unknown as Request, res as unknown as Response);
    return res;
  };
}

describe("POST /incidents/:id/resolve", () => {
  it("resolves the incident as the caller and answers 204", async () => {
    const execute = vi.fn().mockResolvedValue(undefined);
    const res = await resolveRoute(execute)();
    expect(execute).toHaveBeenCalledWith(actor, "i1");
    expect(res.status).toHaveBeenCalledWith(204);
  });

  it("answers 404 for an incident that is missing or of another tenant", async () => {
    const res = await resolveRoute(vi.fn().mockRejectedValue(new NotFoundError("i1")))();
    expect(res.status).toHaveBeenCalledWith(404);
    expect(res.json).toHaveBeenCalledWith({ error: "not_found" });
  });

  it("answers 403 when the caller may not resolve", async () => {
    const res = await resolveRoute(vi.fn().mockRejectedValue(new ForbiddenError("no")))();
    expect(res.status).toHaveBeenCalledWith(403);
    expect(res.json).toHaveBeenCalledWith({ error: "forbidden" });
  });
});
