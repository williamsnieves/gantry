export const SEVERITIES = ["SEV1", "SEV2", "SEV3"] as const;
export type Severity = (typeof SEVERITIES)[number];

export interface Incident {
  id: string;
  tenantId: string;
  title: string;
  severity: Severity;
  priority: number;
  status: "OPEN" | "RESOLVED";
}

export interface Actor {
  userId: string;
  tenantId: string;
  role: "commander" | "responder";
  isSupport: boolean;
}

export class NotFoundError extends Error {}
export class ForbiddenError extends Error {}
