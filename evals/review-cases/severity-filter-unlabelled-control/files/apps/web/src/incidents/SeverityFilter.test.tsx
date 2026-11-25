import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { SeverityFilter } from "./SeverityFilter";

describe("SeverityFilter", () => {
  it("reports the selected severity", async () => {
    const onChange = vi.fn();
    render(<SeverityFilter value={undefined} onChange={onChange} />);
    await userEvent.selectOptions(screen.getByRole("combobox"), "SEV1");
    expect(onChange).toHaveBeenCalledWith("SEV1");
  });

  it("clears the filter when All is selected", async () => {
    const onChange = vi.fn();
    render(<SeverityFilter value="SEV2" onChange={onChange} />);
    await userEvent.selectOptions(screen.getByRole("combobox"), "");
    expect(onChange).toHaveBeenCalledWith(undefined);
  });
});
