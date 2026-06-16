import { render } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { DotWeekStrip } from "../dot-week-strip";

describe("DotWeekStrip", () => {
  it("renders seven bars", () => {
    const { container } = render(
      <MemoryRouter>
        <DotWeekStrip counts={[0, 1, 2, 3, 2, 1, 0]} />
      </MemoryRouter>,
    );
    expect(container.querySelectorAll(".week-rail__day").length).toBe(7);
  });
});
