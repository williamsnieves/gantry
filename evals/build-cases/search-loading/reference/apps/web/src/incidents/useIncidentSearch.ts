import { useEffect, useState } from "react";
import type { IncidentView } from "./api";

export type SearchFn = (query: string, signal: AbortSignal) => Promise<IncidentView[]>;

export interface IncidentSearch {
  results: IncidentView[];
  loading: boolean;
}

/** Returns the incidents matching `query` and whether a search is in flight, ignoring responses for superseded queries. */
export function useIncidentSearch(query: string, search: SearchFn): IncidentSearch {
  const [results, setResults] = useState<IncidentView[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    search(query, controller.signal)
      .then((incidents) => {
        if (!controller.signal.aborted) setResults(incidents);
      })
      .catch(() => {
        // Aborted or failed requests leave the previous results in place.
      })
      .finally(() => {
        // A superseded request does not end the loading of the one that replaced it.
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [query, search]);

  return { results, loading };
}
