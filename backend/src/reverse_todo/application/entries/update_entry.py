from dataclasses import dataclass
from datetime import date
from uuid import UUID

from reverse_todo.domain.entities import Entry
from reverse_todo.domain.errors import EntryNotFoundError
from reverse_todo.domain.repositories import EntryRepository, TagRepository
from reverse_todo.domain.value_objects.category import TagCategory


@dataclass(slots=True)
class UpdateEntryCommand:
    user_id: UUID
    entry_id: UUID
    project_id: UUID | None = None
    tag_ids: list[UUID] | None = None
    category: TagCategory | None = None
    mood: int | None = None
    update_mood: bool = False


class UpdateEntryUseCase:
    def __init__(self, entries: EntryRepository, tags: TagRepository) -> None:
        self._entries = entries
        self._tags = tags

    async def execute(self, command: UpdateEntryCommand) -> Entry:
        entry = await self._entries.get_by_id(command.user_id, command.entry_id)
        if entry is None:
            raise EntryNotFoundError("Entry not found")
        if command.project_id is not None:
            entry.project_id = command.project_id
        if command.tag_ids is not None:
            all_tags = await self._tags.list_by_user(command.user_id)
            tag_map = {t.id: t for t in all_tags}
            entry.tags = [tag_map[tid] for tid in command.tag_ids if tid in tag_map]
        if command.category is not None:
            tag = await self._tags.get_or_create(
                command.user_id, command.category.value, command.category
            )
            entry.tags = [tag]
        if command.update_mood:
            entry.mood = command.mood
        return await self._entries.update(entry)


@dataclass(slots=True)
class ListEntriesQuery:
    user_id: UUID
    date_from: date | None = None
    date_to: date | None = None


class ListEntriesUseCase:
    def __init__(self, entries: EntryRepository) -> None:
        self._entries = entries

    async def execute(self, query: ListEntriesQuery) -> list[Entry]:
        if query.date_from is None and query.date_to is None:
            return await self._entries.list_by_user(query.user_id)
        start = query.date_from or query.date_to
        end = query.date_to or query.date_from
        assert start is not None and end is not None
        return await self._entries.list_by_date_range(query.user_id, start, end)
