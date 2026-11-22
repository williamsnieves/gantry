import { useEffect, useState } from "react";
import type { IncidentView } from "./api";

export type SearchFn = (query: string, signal: AbortSignal) => Promise<IncidentView[]>;

/** Returns the incidents matching `query`, ignoring responses for superseded queries. */
export function useIncidentSearch(query: string, search: SearchFn): IncidentView[] {
  const [results, setResults] = useState<IncidentView[]>([]);

  useEffect(() => {
    const controller = new AbortController();
    search(query, controller.signal)
      .then((incidents) => {
        if (!controller.signal.aborted) setResults(incidents);
      })
      .catch(() => {
        // Aborted or failed requests leave the previous results in place.
      });
    return () => controller.abort();
  }, [query, search]);

  return results;
}
