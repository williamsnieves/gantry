import { ForbiddenError, NotFoundError, type Actor, type Severity } from "./incident";
import type { IncidentRepository } from "./incident-repository";

export class UpdateIncidentSeverity {
  constructor(private readonly incidents: IncidentRepository) {}

  async execute(actor: Actor, incidentId: string, severity: Severity): Promise<void> {
    const incident = await this.incidents.findById(incidentId);
    // Incidents of another tenant are reported as missing so their existence is not disclosed.
    if (!incident || (incident.tenantId !== actor.tenantId && !actor.isSupport)) {
      throw new NotFoundError(incidentId);
    }
    if (actor.role !== "commander") {
      throw new ForbiddenError("Only a commander can change severity.");
    }
    await this.incidents.save({ ...incident, severity });
  }
}
