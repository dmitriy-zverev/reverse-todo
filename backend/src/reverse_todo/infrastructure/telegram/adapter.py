"""Telegram bot adapter — phase 2."""

from uuid import UUID

from reverse_todo.application.entries.create_entry import CreateEntryCommand, CreateEntryUseCase
from reverse_todo.domain.value_objects.source import EntrySource


class TelegramEntryAdapter:
    """Bridges aiogram updates to CreateEntryUseCase."""

    def __init__(self, create_entry: CreateEntryUseCase) -> None:
        self._create_entry = create_entry

    async def handle_text(
        self,
        user_id: UUID,
        timezone: str,
        text: str,
    ) -> str:
        entry, _ = await self._create_entry.execute(
            CreateEntryCommand(
                user_id=user_id,
                timezone=timezone,
                raw_text=text,
                source=EntrySource.TELEGRAM,
            )
        )
        return f"Записано: {entry.raw_text[:80]}"
