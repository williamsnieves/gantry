import { ForbiddenError, NotFoundError, type Actor } from "./incident";
import type { IncidentRepository } from "./incident-repository";

export class ResolveIncident {
  constructor(private readonly incidents: IncidentRepository) {}

  async execute(actor: Actor, incidentId: string): Promise<void> {
    const incident = await this.incidents.findById(incidentId);
    if (!incident) {
      throw new NotFoundError(incidentId);
    }
    if (actor.role !== "commander") {
      throw new ForbiddenError("Only a commander can resolve an incident.");
    }
    if (incident.tenantId !== actor.tenantId) {
      throw new NotFoundError(incidentId);
    }
    if (incident.status === "RESOLVED") {
      return;
    }
    await this.incidents.save({ ...incident, status: "RESOLVED" });
  }
}
