import { QueryClient, QueryClientProvider, useQuery } from "@tanstack/react-query";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { EveningReminder } from "./components/evening-reminder";
import { Layout } from "./components/layout";
import { ArchivePage } from "./pages/archive";
import { AuthPage } from "./pages/auth";
import { TodayPage } from "./pages/today";
import { WeekPage } from "./pages/week";
import { api } from "./api/client";
import "./styles/tokens.css";

const queryClient = new QueryClient();

function AppRoutes() {
  const { data: user, isLoading, isError, refetch } = useQuery({
    queryKey: ["me"],
    queryFn: () => api.me(),
    retry: false,
  });

  if (isLoading) {
    return <p className="p-8 text-center text-sm text-[var(--color-ink-muted)]">…</p>;
  }

  if (isError || !user) {
    return <AuthPage onSuccess={() => void refetch()} />;
  }

  return (
    <>
      <EveningReminder user={user} />
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<TodayPage />} />
          <Route path="week" element={<WeekPage />} />
          <Route path="archive" element={<ArchivePage />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </QueryClientProvider>
  );
}
