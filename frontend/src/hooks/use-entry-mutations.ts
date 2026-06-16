import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../api/client";
import type { TagCategory } from "../api/types";

export interface UpdateEntryPatch {
  mood?: number | null;
  category?: TagCategory;
}

export function useEntryMutations() {
  const queryClient = useQueryClient();

  function invalidateAll() {
    void queryClient.invalidateQueries({ queryKey: ["today"] });
    void queryClient.invalidateQueries({ queryKey: ["weekly"] });
    void queryClient.invalidateQueries({ queryKey: ["archive"] });
  }

  const updateEntry = useMutation({
    mutationFn: ({ id, patch }: { id: string; patch: UpdateEntryPatch }) =>
      api.updateEntry(id, patch),
    onSuccess: invalidateAll,
  });

  const deleteEntry = useMutation({
    mutationFn: (id: string) => api.deleteEntry(id),
    onSuccess: invalidateAll,
  });

  return { updateEntry, deleteEntry };
}

export type EntryMutations = ReturnType<typeof useEntryMutations>;
