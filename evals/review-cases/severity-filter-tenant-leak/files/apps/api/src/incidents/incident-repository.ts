import type { Incident, Severity } from "./incident";

export interface IncidentRepository {
  findById(id: string): Promise<Incident | null>;
  listByTenant(tenantId: string, filter?: { severity?: Severity }): Promise<Incident[]>;
  save(incident: Incident): Promise<void>;
}
