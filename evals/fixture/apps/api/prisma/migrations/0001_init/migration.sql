CREATE TABLE "Incident" (
  "id" TEXT PRIMARY KEY,
  "tenantId" TEXT NOT NULL,
  "title" TEXT NOT NULL,
  "severity" TEXT NOT NULL,
  "status" TEXT NOT NULL DEFAULT 'OPEN',
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updatedAt" TIMESTAMP(3) NOT NULL
);

CREATE INDEX "Incident_tenantId_status_idx" ON "Incident" ("tenantId", "status");
