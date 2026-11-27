import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { listIncidents } from "./api";
import { SeverityFilter } from "./SeverityFilter";

afterEach(() => vi.unstubAllGlobals());

function stubFetch() {
  const fetchMock = vi.fn().mockResolvedValue({ ok: true, status: 200, json: async () => [] });
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

describe("listIncidents (hidden)", () => {
  it("requests the full list when no filter is given", async () => {
    const fetchMock = stubFetch();
    await listIncidents();
    expect(fetchMock.mock.calls[0][0]).toBe("/api/incidents");
  });

  it("sends the severity as a query parameter", async () => {
    const fetchMock = stubFetch();
    await listIncidents({ severity: "SEV1" });
    expect(fetchMock.mock.calls[0][0]).toBe("/api/incidents?severity=SEV1");
  });

  it("[edge] still forwards the abort signal", async () => {
    const fetchMock = stubFetch();
    const { signal } = new AbortController();
    await listIncidents({}, signal);
    expect(fetchMock.mock.calls[0][1]?.signal).toBe(signal);
  });
});

describe("SeverityFilter (hidden)", () => {
  it("offers All and the three severities", () => {
    render(<SeverityFilter value={undefined} onChange={() => {}} />);
    expect(screen.getAllByRole("option").map((option) => option.textContent)).toEqual(["All", "SEV1", "SEV2", "SEV3"]);
  });

  it("reports the chosen severity, and undefined for All", async () => {
    const onChange = vi.fn();
    render(<SeverityFilter value="SEV1" onChange={onChange} />);
    await userEvent.selectOptions(screen.getByRole("combobox"), "SEV2");
    expect(onChange).toHaveBeenLastCalledWith("SEV2");
    await userEvent.selectOptions(screen.getByRole("combobox"), "All");
    expect(onChange).toHaveBeenLastCalledWith(undefined);
  });

  it("[edge] has an accessible name that says what it filters", () => {
    render(<SeverityFilter value={undefined} onChange={() => {}} />);
    expect(screen.getByRole("combobox", { name: /severity/i })).toBeInTheDocument();
  });
});
