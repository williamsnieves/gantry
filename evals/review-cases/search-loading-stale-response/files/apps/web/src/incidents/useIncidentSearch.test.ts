import { renderHook, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import type { IncidentView } from "./api";
import { useIncidentSearch, type SearchFn } from "./useIncidentSearch";

const apiDown: IncidentView = { id: "i1", title: "API down", severity: "SEV1", status: "OPEN" };
const slowQueue: IncidentView = { id: "i2", title: "Slow queue", severity: "SEV3", status: "OPEN" };

describe("useIncidentSearch", () => {
  it("is loading until the search answers, then returns its results", async () => {
    const search: SearchFn = vi.fn().mockResolvedValue([apiDown]);
    const { result } = renderHook(() => useIncidentSearch("api", search));
    expect(result.current).toEqual({ results: [], loading: true });
    await waitFor(() => expect(result.current).toEqual({ results: [apiDown], loading: false }));
  });

  it("searches again when the query changes and aborts the earlier request", async () => {
    const signals: AbortSignal[] = [];
    const search: SearchFn = vi.fn(async (query, signal) => {
      signals.push(signal);
      return query === "api" ? [apiDown] : [slowQueue];
    });
    const { result, rerender } = renderHook(({ query }) => useIncidentSearch(query, search), { initialProps: { query: "api" } });
    await waitFor(() => expect(result.current.results).toEqual([apiDown]));
    rerender({ query: "queue" });
    await waitFor(() => expect(result.current).toEqual({ results: [slowQueue], loading: false }));
    expect(signals[0].aborted).toBe(true);
  });

  it("keeps the previous results and stops loading when a search fails", async () => {
    const search: SearchFn = vi.fn(async (query) => {
      if (query === "boom") throw new Error("network");
      return [apiDown];
    });
    const { result, rerender } = renderHook(({ query }) => useIncidentSearch(query, search), { initialProps: { query: "api" } });
    await waitFor(() => expect(result.current.results).toEqual([apiDown]));
    rerender({ query: "boom" });
    await waitFor(() => expect(result.current.loading).toBe(false));
    expect(result.current.results).toEqual([apiDown]);
  });
});
