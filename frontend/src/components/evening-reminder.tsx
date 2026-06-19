import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../api/client";
import type { User } from "../api/types";
import { useEveningReminder } from "../hooks/use-evening-reminder";
import { EveningReminderModal } from "./evening-reminder-modal";

interface EveningReminderProps {
  user: User;
}

export function EveningReminder({ user }: EveningReminderProps) {
  const queryClient = useQueryClient();
  const { open, dismiss, disable, close } = useEveningReminder(user.id, user.timezone);

  const create = useMutation({
    mutationFn: ({ text, mood }: { text: string; mood?: number }) => api.createEntry(text, mood),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["today"] });
      void queryClient.invalidateQueries({ queryKey: ["weekly"] });
      void queryClient.invalidateQueries({ queryKey: ["archive"] });
      close();
    },
  });

  return (
    <EveningReminderModal
      open={open}
      onDismiss={dismiss}
      onDisable={disable}
      onSubmit={async (text, mood) => {
        await create.mutateAsync({ text, mood });
      }}
    />
  );
}
