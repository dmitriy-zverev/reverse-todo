import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { CategoryBars } from "../category-bars";

describe("CategoryBars", () => {
  it("renders categories", () => {
    render(
      <CategoryBars
        items={[
          { category: "work", count: 5 },
          { category: "health", count: 2 },
        ]}
      />,
    );
    expect(screen.getByText("работа")).toBeInTheDocument();
    expect(screen.getByText("5")).toBeInTheDocument();
  });
});
