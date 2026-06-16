import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { ENTRY_FIELD_LABEL } from "../../lib/entry-prompts";
import { EntryComposer } from "../entry-composer";

describe("EntryComposer", () => {
  it("submits text", async () => {
    const onSubmit = vi.fn().mockResolvedValue(undefined);
    const user = userEvent.setup();
    render(<EntryComposer onSubmit={onSubmit} />);
    await user.type(screen.getByLabelText(ENTRY_FIELD_LABEL), "сверстан макет");
    await user.click(screen.getByRole("button", { name: "Записать" }));
    expect(onSubmit).toHaveBeenCalledWith("сверстан макет", undefined);
  });

  it("adds custom chip from plus button", async () => {
    const onSubmit = vi.fn().mockResolvedValue(undefined);
    const user = userEvent.setup();
    render(<EntryComposer onSubmit={onSubmit} />);
    await user.click(screen.getByRole("button", { name: "Добавить свою подсказку" }));
    await user.type(screen.getByLabelText("Своя подсказка"), "код-ревью");
    await user.click(screen.getByRole("button", { name: "Сохранить подсказку" }));
    await user.click(screen.getByRole("button", { name: "Записать" }));
    expect(onSubmit).toHaveBeenCalledWith("код-ревью", undefined);
  });

  it("submits selected mood", async () => {
    const onSubmit = vi.fn().mockResolvedValue(undefined);
    const user = userEvent.setup();
    render(<EntryComposer onSubmit={onSubmit} />);
    await user.type(screen.getByLabelText(ENTRY_FIELD_LABEL), "отдых");
    await user.click(screen.getByRole("button", { name: "устало" }));
    await user.click(screen.getByRole("button", { name: "Записать" }));
    expect(onSubmit).toHaveBeenCalledWith("отдых", 4);
  });
});
