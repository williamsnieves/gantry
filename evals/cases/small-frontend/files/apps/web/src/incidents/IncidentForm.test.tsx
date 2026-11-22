import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { IncidentForm } from "./IncidentForm";

describe("IncidentForm", () => {
  it("submits the title and severity", async () => {
    const onSubmit = vi.fn();
    render(<IncidentForm onSubmit={onSubmit} />);
    await userEvent.type(screen.getByLabelText("Title"), "API down");
    await userEvent.click(screen.getByRole("button", { name: "Create incident" }));
    expect(onSubmit).toHaveBeenCalledWith({ title: "API down", severity: "SEV3" });
  });

  it("trims the title before submitting", async () => {
    const onSubmit = vi.fn();
    render(<IncidentForm onSubmit={onSubmit} />);
    await userEvent.type(screen.getByLabelText("Title"), "  API down  ");
    await userEvent.click(screen.getByRole("button", { name: "Create incident" }));
    expect(onSubmit).toHaveBeenCalledWith({ title: "API down", severity: "SEV3" });
  });

  it("rejects titles shorter than 3 characters", async () => {
    const onSubmit = vi.fn();
    render(<IncidentForm onSubmit={onSubmit} />);
    await userEvent.type(screen.getByLabelText("Title"), " ab ");
    await userEvent.click(screen.getByRole("button", { name: "Create incident" }));
    expect(screen.getByRole("alert")).toHaveTextContent("Title must be at least 3 characters.");
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("requires a title", async () => {
    const onSubmit = vi.fn();
    render(<IncidentForm onSubmit={onSubmit} />);
    await userEvent.click(screen.getByRole("button", { name: "Create incident" }));
    expect(screen.getByRole("alert")).toHaveTextContent("Title is required.");
    expect(onSubmit).not.toHaveBeenCalled();
  });
});
