import pytest

from reverse_todo.infrastructure.telegram.adapter import TelegramEntryAdapter
from reverse_todo.application.entries.create_entry import CreateEntryUseCase
from reverse_todo.infrastructure.classification.rules import RuleBasedClassifier
from tests.fakes import FakeStore


@pytest.mark.asyncio
async def test_telegram_adapter():
    store = FakeStore()
    uc = CreateEntryUseCase(
        store.entries, store.tags, store.projects, store.skills, RuleBasedClassifier()
    )
    adapter = TelegramEntryAdapter(uc)
    from uuid import uuid4

    msg = await adapter.handle_text(uuid4(), "UTC", "сделал деплой")
    assert "Записано" in msg
