import { ForbiddenError, NotFoundError, type Actor } from "./incident";
import type { IncidentRepository } from "./incident-repository";

export class ResolveIncident {
  constructor(private readonly incidents: IncidentRepository) {}

  async execute(actor: Actor, incidentId: string): Promise<void> {
    const incident = await this.incidents.findById(incidentId);
    // Incidents of another tenant are reported as missing so their existence is not disclosed.
    if (!incident || incident.tenantId !== actor.tenantId) {
      throw new NotFoundError(incidentId);
    }
    if (actor.role !== "commander") {
      throw new ForbiddenError("Only a commander can resolve an incident.");
    }
    if (incident.status === "RESOLVED") {
      return;
    }
    await this.incidents.save({ ...incident, status: "RESOLVED" });
  }
}
