export interface IncidentView {
  id: string;
  title: string;
  severity: "SEV1" | "SEV2" | "SEV3";
  status: "OPEN" | "RESOLVED";
}

export async function listIncidents(
  filter: { severity?: IncidentView["severity"] } = {},
  signal?: AbortSignal,
): Promise<IncidentView[]> {
  const query = filter.severity ? `?severity=${encodeURIComponent(filter.severity)}` : "";
  const response = await fetch(`/api/incidents${query}`, { signal });
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
