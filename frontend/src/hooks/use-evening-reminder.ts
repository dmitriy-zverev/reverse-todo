import { useQuery } from "@tanstack/react-query";
import { useCallback, useEffect, useState } from "react";
import { api } from "../api/client";
import {
  loadDismissedDateKey,
  loadReminderEnabled,
  localTimeParts,
  saveDismissedDateKey,
  saveReminderEnabled,
  shouldShowEveningReminder,
} from "../lib/evening-reminder";

export function useEveningReminder(userId: string, timeZone: string) {
  const [enabled, setEnabledState] = useState(() => loadReminderEnabled());
  const [dismissedDateKey, setDismissedDateKey] = useState<string | null>(() =>
    loadDismissedDateKey(userId),
  );
  const [latchedOpen, setLatchedOpen] = useState(false);
  const [tick, setTick] = useState(0);

  const { data: today } = useQuery({
    queryKey: ["today"],
    queryFn: () => api.todaySummary(),
    refetchInterval: 60_000,
  });

  const entryCount = today?.entry_count ?? 0;

  const shouldShow = shouldShowEveningReminder({
    timeZone,
    entryCount,
    enabled,
    dismissedDateKey,
  });

  useEffect(() => {
    setDismissedDateKey(loadDismissedDateKey(userId));
  }, [userId]);

  useEffect(() => {
    const id = window.setInterval(() => setTick((value) => value + 1), 60_000);
    const onVisibility = () => setTick((value) => value + 1);
    document.addEventListener("visibilitychange", onVisibility);
    return () => {
      window.clearInterval(id);
      document.removeEventListener("visibilitychange", onVisibility);
    };
  }, []);

  useEffect(() => {
    if (shouldShow) {
      setLatchedOpen(true);
    }
  }, [shouldShow, tick]);

  useEffect(() => {
    if (entryCount > 0) {
      setLatchedOpen(false);
    }
  }, [entryCount]);

  const dismiss = useCallback(() => {
    const { dateKey } = localTimeParts(timeZone);
    saveDismissedDateKey(userId, dateKey);
    setDismissedDateKey(dateKey);
    setLatchedOpen(false);
  }, [userId, timeZone]);

  const disable = useCallback(() => {
    saveReminderEnabled(false);
    setEnabledState(false);
    setLatchedOpen(false);
  }, []);

  const close = useCallback(() => {
    setLatchedOpen(false);
  }, []);

  const open = latchedOpen && shouldShow;

  return { open, dismiss, disable, close };
}
