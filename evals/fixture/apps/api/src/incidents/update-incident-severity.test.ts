import { describe, expect, it } from "vitest";
import { ForbiddenError, NotFoundError, type Actor, type Incident } from "./incident";
import type { IncidentRepository } from "./incident-repository";
import { UpdateIncidentSeverity } from "./update-incident-severity";

class InMemoryIncidents implements IncidentRepository {
  constructor(private readonly rows: Incident[]) {}
  async findById(id: string) {
    return this.rows.find((row) => row.id === id) ?? null;
  }
  async listByTenant(tenantId: string) {
    return this.rows.filter((row) => row.tenantId === tenantId);
  }
  async save(incident: Incident) {
    this.rows.splice(this.rows.findIndex((row) => row.id === incident.id), 1, incident);
  }
}

const incident: Incident = { id: "i1", tenantId: "t1", title: "API down", severity: "SEV3", status: "OPEN" };
const commander: Actor = { userId: "u1", tenantId: "t1", role: "commander", isSupport: false };

describe("UpdateIncidentSeverity", () => {
  it("lets a commander of the same tenant change severity", async () => {
    const incidents = new InMemoryIncidents([{ ...incident }]);
    await new UpdateIncidentSeverity(incidents).execute(commander, "i1", "SEV1");
    expect((await incidents.findById("i1"))?.severity).toBe("SEV1");
  });

  it("hides incidents of another tenant", async () => {
    const incidents = new InMemoryIncidents([{ ...incident }]);
    const outsider = { ...commander, tenantId: "t2" };
    await expect(new UpdateIncidentSeverity(incidents).execute(outsider, "i1", "SEV1")).rejects.toBeInstanceOf(NotFoundError);
  });

  it("rejects responders", async () => {
    const incidents = new InMemoryIncidents([{ ...incident }]);
    const responder = { ...commander, role: "responder" as const };
    await expect(new UpdateIncidentSeverity(incidents).execute(responder, "i1", "SEV1")).rejects.toBeInstanceOf(ForbiddenError);
  });
});
