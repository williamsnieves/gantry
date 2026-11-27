import { act, renderHook, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import type { IncidentView } from "./api";
import { useIncidentSearch, type SearchFn } from "./useIncidentSearch";

const apiDown: IncidentView = { id: "i1", title: "API down", severity: "SEV1", status: "OPEN" };
const slowQueue: IncidentView = { id: "i2", title: "Slow queue", severity: "SEV3", status: "OPEN" };

/** A search whose answers are given by hand, in any order, and that ignores the abort signal. */
function manualSearch() {
  const pending = new Map<string, { resolve(value: IncidentView[]): void; reject(error: Error): void }>();
  const search: SearchFn = (query) => new Promise((resolve, reject) => pending.set(query, { resolve, reject }));
  return { search, answer: (query: string, value: IncidentView[]) => act(async () => pending.get(query)!.resolve(value)),
           fail: (query: string) => act(async () => pending.get(query)!.reject(new Error("network"))) };
}

describe("useIncidentSearch (hidden)", () => {
  it("is loading until the search answers, then returns its results", async () => {
    const search: SearchFn = vi.fn().mockResolvedValue([apiDown]);
    const { result } = renderHook(() => useIncidentSearch("api", search));
    expect(result.current.loading).toBe(true);
    expect(result.current.results).toEqual([]);
    await waitFor(() => expect(result.current.loading).toBe(false));
    expect(result.current.results).toEqual([apiDown]);
  });

  it("aborts the request of a superseded query", async () => {
    const signals: AbortSignal[] = [];
    const search: SearchFn = async (_query, signal) => {
      signals.push(signal);
      return [];
    };
    const { rerender } = renderHook(({ query }) => useIncidentSearch(query, search), { initialProps: { query: "api" } });
    rerender({ query: "queue" });
    await waitFor(() => expect(signals.length).toBe(2));
    expect(signals[0].aborted).toBe(true);
    expect(signals[1].aborted).toBe(false);
  });

  it("keeps the previous results and stops loading when a search fails", async () => {
    const manual = manualSearch();
    const { result, rerender } = renderHook(({ query }) => useIncidentSearch(query, manual.search), { initialProps: { query: "api" } });
    await manual.answer("api", [apiDown]);
    rerender({ query: "boom" });
    expect(result.current.loading).toBe(true);
    await manual.fail("boom");
    expect(result.current.loading).toBe(false);
    expect(result.current.results).toEqual([apiDown]);
  });

  it("[edge] ignores the answer to a superseded query that arrives after the current one", async () => {
    const manual = manualSearch();
    const { result, rerender } = renderHook(({ query }) => useIncidentSearch(query, manual.search), { initialProps: { query: "api" } });
    rerender({ query: "queue" });
    await manual.answer("queue", [slowQueue]);
    await manual.answer("api", [apiDown]);
    expect(result.current.results).toEqual([slowQueue]);
  });

  it("[edge] stays loading when a superseded query answers while the current one is in flight", async () => {
    const manual = manualSearch();
    const { result, rerender } = renderHook(({ query }) => useIncidentSearch(query, manual.search), { initialProps: { query: "api" } });
    rerender({ query: "queue" });
    await manual.answer("api", [apiDown]);
    expect(result.current.loading).toBe(true);
    expect(result.current.results).toEqual([]);
    await manual.answer("queue", [slowQueue]);
    expect(result.current.loading).toBe(false);
  });

  it("[edge] stays loading when a superseded query fails while the current one is in flight", async () => {
    const manual = manualSearch();
    const { result, rerender } = renderHook(({ query }) => useIncidentSearch(query, manual.search), { initialProps: { query: "api" } });
    rerender({ query: "queue" });
    await manual.fail("api");
    expect(result.current.loading).toBe(true);
  });
});
