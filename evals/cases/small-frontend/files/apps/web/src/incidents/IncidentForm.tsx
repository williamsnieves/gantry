import { useState, type FormEvent } from "react";
import type { IncidentView } from "./api";

interface Props {
  onSubmit(input: { title: string; severity: IncidentView["severity"] }): void;
}

export function IncidentForm({ onSubmit }: Props) {
  const [title, setTitle] = useState("");
  const [severity, setSeverity] = useState<IncidentView["severity"]>("SEV3");
  const [error, setError] = useState<string | null>(null);

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const trimmed = title.trim();
    if (trimmed.length === 0) {
      setError("Title is required.");
      return;
    }
    if (trimmed.length < 3) {
      setError("Title must be at least 3 characters.");
      return;
    }
    setError(null);
    onSubmit({ title: trimmed, severity });
  }

  return (
    <form onSubmit={handleSubmit} aria-label="New incident">
      <label htmlFor="incident-title">Title</label>
      <input
        id="incident-title"
        value={title}
        onChange={(event) => setTitle(event.target.value)}
        aria-invalid={error !== null}
        aria-describedby={error ? "incident-title-error" : undefined}
      />
      {error && (
        <p id="incident-title-error" role="alert">
          {error}
        </p>
      )}
      <label htmlFor="incident-severity">Severity</label>
      <select
        id="incident-severity"
        value={severity}
        onChange={(event) => setSeverity(event.target.value as IncidentView["severity"])}
      >
        <option value="SEV1">SEV1</option>
        <option value="SEV2">SEV2</option>
        <option value="SEV3">SEV3</option>
      </select>
      <button type="submit">Create incident</button>
    </form>
  );
}
