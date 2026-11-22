import type { PrismaClient } from "@prisma/client";
import type { Incident, Severity } from "./incident";
import type { IncidentRepository } from "./incident-repository";

type Row = { id: string; tenantId: string; title: string; severity: string; priority: number; status: string };

const toIncident = (row: Row): Incident => ({
  id: row.id,
  tenantId: row.tenantId,
  title: row.title,
  severity: row.severity as Severity,
  priority: row.priority,
  status: row.status as Incident["status"],
});

export class PrismaIncidentRepository implements IncidentRepository {
  constructor(private readonly prisma: PrismaClient) {}

  async findById(id: string): Promise<Incident | null> {
    const row = await this.prisma.incident.findUnique({ where: { id } });
    return row ? toIncident(row) : null;
  }

  async listByTenant(tenantId: string): Promise<Incident[]> {
    const rows = await this.prisma.incident.findMany({ where: { tenantId }, orderBy: { createdAt: "desc" } });
    return rows.map(toIncident);
  }

  async save(incident: Incident): Promise<void> {
    await this.prisma.incident.upsert({
      where: { id: incident.id },
      create: incident,
      update: { title: incident.title, severity: incident.severity, priority: incident.priority, status: incident.status },
    });
  }
}
