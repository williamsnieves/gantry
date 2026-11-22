import type { Incident } from "./incident";

export interface IncidentRepository {
  findById(id: string): Promise<Incident | null>;
  listByTenant(tenantId: string): Promise<Incident[]>;
  save(incident: Incident): Promise<void>;
}
