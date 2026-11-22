import { renderHook, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import type { IncidentView } from "./api";
import { useIncidentSearch, type SearchFn } from "./useIncidentSearch";

const incident = (id: string): IncidentView => ({ id, title: id, severity: "SEV3", status: "OPEN" });

describe("useIncidentSearch", () => {
  // Regression test for the stale-response race reported in the last QA review:
  // a slow response for an earlier query must not overwrite a newer one.
  it("ignores a slow response for a superseded query", async () => {
    const resolvers: Record<string, (value: IncidentView[]) => void> = {};
    const search: SearchFn = (query) => new Promise((resolve) => (resolvers[query] = resolve));

    const { result, rerender } = renderHook(({ query }) => useIncidentSearch(query, search), {
      initialProps: { query: "a" },
    });
    rerender({ query: "ab" });

    resolvers["ab"]([incident("newer")]);
    await waitFor(() => expect(result.current).toEqual([incident("newer")]));

    resolvers["a"]([incident("stale")]);
    await Promise.resolve();
    expect(result.current).toEqual([incident("newer")]);
  });
});
