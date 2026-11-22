export interface IncidentView {
  id: string;
  title: string;
  severity: "SEV1" | "SEV2" | "SEV3";
  status: "OPEN" | "RESOLVED";
}

export async function listIncidents(signal?: AbortSignal): Promise<IncidentView[]> {
  const response = await fetch("/api/incidents", { signal });
  if (!response.ok) throw new Error(`Failed to load incidents (${response.status})`);
  return response.json();
}

export async function createIncident(input: { title: string; severity: IncidentView["severity"] }): Promise<void> {
  const response = await fetch("/api/incidents", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(input),
  });
  if (!response.ok) throw new Error(`Failed to create incident (${response.status})`);
}
