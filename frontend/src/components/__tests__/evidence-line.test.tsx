import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { EvidenceLine } from "../evidence-line";

const entry = {
  id: "1",
  raw_text: "починил баг",
  entry_date: "2025-06-15",
  source: "web",
  mood: 3,
  energy: null,
  project_id: null,
  tags: [{ id: "t1", name: "work", category: "work" as const }],
  skills: [],
  created_at: "2025-06-15T12:00:00Z",
};

function renderLine() {
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
  return render(
    <QueryClientProvider client={client}>
      <EvidenceLine entry={entry} />
    </QueryClientProvider>,
  );
}

describe("EvidenceLine", () => {
  it("renders entry text and metadata", () => {
    renderLine();
    expect(screen.getByText("починил баг")).toBeInTheDocument();
    expect(screen.getAllByText("работа").length).toBeGreaterThan(0);
    expect(screen.getByLabelText("нормально")).toBeInTheDocument();
  });

  it("renders entry controls", () => {
    renderLine();
    expect(screen.getByLabelText("Управление записью")).toBeInTheDocument();
    expect(screen.getByLabelText("Категория: работа")).toBeInTheDocument();
    expect(screen.getByLabelText("Удалить запись")).toBeInTheDocument();
  });
});
