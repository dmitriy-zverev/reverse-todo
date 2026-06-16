import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { api } from "../api/client";

export function AuthPage({ onSuccess }: { onSuccess: () => void }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mode, setMode] = useState<"login" | "register">("register");

  const auth = useMutation({
    mutationFn: () =>
      mode === "register" ? api.register(email, password) : api.login(email, password),
    onSuccess,
  });

  return (
    <div className="mx-auto flex min-h-screen max-w-sm flex-col justify-center px-4">
      <h1 className="font-display mb-8 text-3xl">Reverse To-Do</h1>
      <form
        className="space-y-4"
        onSubmit={(e) => {
          e.preventDefault();
          auth.mutate();
        }}
      >
        <input
          type="email"
          required
          placeholder="Email"
          className="w-full border-b border-[var(--color-border)] bg-transparent py-2 outline-none"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          required
          minLength={8}
          placeholder="Пароль"
          className="w-full border-b border-[var(--color-border)] bg-transparent py-2 outline-none"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          type="submit"
          className="w-full rounded-full bg-[var(--color-accent)] py-2 text-[var(--color-on-accent)]"
        >
          {mode === "register" ? "Создать аккаунт" : "Войти"}
        </button>
      </form>
      <button
        type="button"
        className="mt-4 text-sm text-[var(--color-ink-muted)]"
        onClick={() => setMode(mode === "register" ? "login" : "register")}
      >
        {mode === "register" ? "Уже есть аккаунт" : "Новый аккаунт"}
      </button>
    </div>
  );
}
