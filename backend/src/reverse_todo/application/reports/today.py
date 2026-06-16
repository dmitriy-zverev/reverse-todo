from dataclasses import dataclass
from datetime import date
from uuid import UUID

from reverse_todo.domain.entities import Entry, TodaySummary
from reverse_todo.domain.repositories import EntryRepository
from reverse_todo.domain.value_objects.entry_date import EntryDate


@dataclass(slots=True)
class CreateEntryCommand:
    user_id: UUID
    timezone: str
    raw_text: str
    source: str
    entry_date: date | None = None
    mood: int | None = None
    energy: int | None = None


class GetTodaySummaryUseCase:
    def __init__(self, entries: EntryRepository) -> None:
        self._entries = entries

    async def execute(self, user_id: UUID, timezone: str) -> TodaySummary:
        today = EntryDate.today_in_timezone(timezone).value
        items = await self._entries.list_by_date_range(user_id, today, today)
        return TodaySummary(entry_date=today, entry_count=len(items), entries=tuple(items))
