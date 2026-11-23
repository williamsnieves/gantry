import { describe, expect, it, vi } from "vitest";
import { PrismaIncidentRepository } from "./prisma-incident-repository";

function repository() {
  const findMany = vi.fn().mockResolvedValue([]);
  const prisma = { incident: { findMany } } as never;
  return { findMany, incidents: new PrismaIncidentRepository(prisma) };
}

describe("PrismaIncidentRepository.listByTenant", () => {
  it("lists every incident of the tenant when no filter is given", async () => {
    const { findMany, incidents } = repository();
    await incidents.listByTenant("t1");
    expect(findMany).toHaveBeenCalledWith({ where: { tenantId: "t1" }, orderBy: { createdAt: "desc" } });
  });

  it("narrows by severity", async () => {
    const { findMany, incidents } = repository();
    await incidents.listByTenant("t1", { severity: "SEV1" });
    expect(findMany).toHaveBeenCalledWith(
      expect.objectContaining({ where: expect.objectContaining({ severity: "SEV1" }) }),
    );
  });
});
