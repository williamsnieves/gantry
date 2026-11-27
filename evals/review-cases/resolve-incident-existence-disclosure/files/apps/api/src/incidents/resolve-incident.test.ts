import { describe, expect, it, vi } from "vitest";
import { ForbiddenError, NotFoundError, type Actor, type Incident } from "./incident";
import type { IncidentRepository } from "./incident-repository";
import { ResolveIncident } from "./resolve-incident";

class InMemoryIncidents implements IncidentRepository {
  readonly save = vi.fn(async (incident: Incident) => {
    this.rows.splice(this.rows.findIndex((row) => row.id === incident.id), 1, incident);
  });
  constructor(private readonly rows: Incident[]) {}
  async findById(id: string) {
    return this.rows.find((row) => row.id === id) ?? null;
  }
  async listByTenant(tenantId: string) {
    return this.rows.filter((row) => row.tenantId === tenantId);
  }
}

const incident: Incident = { id: "i1", tenantId: "t1", title: "API down", severity: "SEV2", status: "OPEN" };
const commander: Actor = { userId: "u1", tenantId: "t1", role: "commander", isSupport: false };

describe("ResolveIncident", () => {
  it("lets a commander of the same tenant resolve an open incident", async () => {
    const incidents = new InMemoryIncidents([{ ...incident }]);
    await new ResolveIncident(incidents).execute(commander, "i1");
    expect((await incidents.findById("i1"))?.status).toBe("RESOLVED");
  });

  it("keeps the other fields of the incident", async () => {
    const incidents = new InMemoryIncidents([{ ...incident }]);
    await new ResolveIncident(incidents).execute(commander, "i1");
    expect(await incidents.findById("i1")).toEqual({ ...incident, status: "RESOLVED" });
  });

  it("does nothing when the incident is already resolved", async () => {
    const incidents = new InMemoryIncidents([{ ...incident, status: "RESOLVED" }]);
    await new ResolveIncident(incidents).execute(commander, "i1");
    expect(incidents.save).not.toHaveBeenCalled();
  });

  it("reports a missing incident", async () => {
    const incidents = new InMemoryIncidents([]);
    await expect(new ResolveIncident(incidents).execute(commander, "i1")).rejects.toBeInstanceOf(NotFoundError);
  });

  it("hides incidents of another tenant", async () => {
    const incidents = new InMemoryIncidents([{ ...incident }]);
    const outsider = { ...commander, tenantId: "t2" };
    await expect(new ResolveIncident(incidents).execute(outsider, "i1")).rejects.toBeInstanceOf(NotFoundError);
    expect(incidents.save).not.toHaveBeenCalled();
  });

  it("rejects responders", async () => {
    const incidents = new InMemoryIncidents([{ ...incident }]);
    const responder = { ...commander, role: "responder" as const };
    await expect(new ResolveIncident(incidents).execute(responder, "i1")).rejects.toBeInstanceOf(ForbiddenError);
    expect(incidents.save).not.toHaveBeenCalled();
  });
});
