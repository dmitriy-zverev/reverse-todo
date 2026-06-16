from dataclasses import dataclass
from uuid import UUID

from reverse_todo.domain.errors import EntryNotFoundError
from reverse_todo.domain.repositories import EntryRepository


@dataclass(slots=True)
class DeleteEntryCommand:
    user_id: UUID
    entry_id: UUID


class DeleteEntryUseCase:
    def __init__(self, entries: EntryRepository) -> None:
        self._entries = entries

    async def execute(self, command: DeleteEntryCommand) -> None:
        deleted = await self._entries.delete(command.user_id, command.entry_id)
        if not deleted:
            raise EntryNotFoundError("Entry not found")
