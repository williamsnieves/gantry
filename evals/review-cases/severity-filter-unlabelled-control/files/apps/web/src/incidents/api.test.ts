import { afterEach, describe, expect, it, vi } from "vitest";
import { listIncidents } from "./api";

function stubFetch(ok = true, status = 200) {
  const fetchMock = vi.fn().mockResolvedValue({ ok, status, json: async () => [] });
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

afterEach(() => vi.unstubAllGlobals());

describe("listIncidents", () => {
  it("requests the full list when no filter is given", async () => {
    const fetchMock = stubFetch();
    await listIncidents();
    expect(fetchMock).toHaveBeenCalledWith("/api/incidents", { signal: undefined });
  });

  it("sends the severity as a query parameter", async () => {
    const fetchMock = stubFetch();
    await listIncidents({ severity: "SEV1" });
    expect(fetchMock).toHaveBeenCalledWith("/api/incidents?severity=SEV1", { signal: undefined });
  });

  it("forwards the abort signal", async () => {
    const fetchMock = stubFetch();
    const { signal } = new AbortController();
    await listIncidents({}, signal);
    expect(fetchMock).toHaveBeenCalledWith("/api/incidents", { signal });
  });

  it("throws when the response is not ok", async () => {
    stubFetch(false, 500);
    await expect(listIncidents()).rejects.toThrow("Failed to load incidents (500)");
  });
});
