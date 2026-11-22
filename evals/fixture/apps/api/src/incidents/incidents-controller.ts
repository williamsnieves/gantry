import type { Request, Response, Router } from "express";
import { z } from "zod";
import { ForbiddenError, NotFoundError, SEVERITIES, type Actor } from "./incident";
import type { IncidentRepository } from "./incident-repository";
import type { UpdateIncidentSeverity } from "./update-incident-severity";

const severityBody = z.object({ severity: z.enum(SEVERITIES) });

// `req.actor` is set by the authentication middleware from the verified session.
type AuthedRequest = Request & { actor: Actor };

export function registerIncidentRoutes(
  router: Router,
  incidents: IncidentRepository,
  updateSeverity: UpdateIncidentSeverity,
): void {
  router.get("/incidents", async (req: Request, res: Response) => {
    const { actor } = req as AuthedRequest;
    res.json(await incidents.listByTenant(actor.tenantId));
  });

  router.patch("/incidents/:id/severity", async (req: Request, res: Response) => {
    const { actor } = req as AuthedRequest;
    const body = severityBody.safeParse(req.body);
    if (!body.success) {
      res.status(400).json({ error: "invalid_severity" });
      return;
    }
    try {
      await updateSeverity.execute(actor, req.params.id, body.data.severity);
      res.status(204).end();
    } catch (error) {
      if (error instanceof NotFoundError) res.status(404).json({ error: "not_found" });
      else if (error instanceof ForbiddenError) res.status(403).json({ error: "forbidden" });
      else throw error;
    }
  });
}
