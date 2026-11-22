import type { IncidentView } from "./api";

type Severity = IncidentView["severity"];

interface Props {
  value: Severity | undefined;
  onChange(value: Severity | undefined): void;
}

export function SeverityFilter({ value, onChange }: Props) {
  return (
    <>
      <label htmlFor="severity-filter">Filter by severity</label>
      <select
        id="severity-filter"
        value={value ?? ""}
        onChange={(event) => onChange(event.target.value === "" ? undefined : (event.target.value as Severity))}
      >
        <option value="">All</option>
        <option value="SEV1">SEV1</option>
        <option value="SEV2">SEV2</option>
        <option value="SEV3">SEV3</option>
      </select>
    </>
  );
}
