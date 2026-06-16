import pytest

from reverse_todo.infrastructure.classification.llm import LLMClassifierStub
from reverse_todo.application.classification.context import DefaultUserContext
from uuid import uuid4


@pytest.mark.asyncio
async def test_llm_stub_delegates_to_rules():
    stub = LLMClassifierStub()
    ctx = DefaultUserContext(user_id=uuid4(), timezone="UTC", projects=[], tags=[], skills=[])
    result = await stub.classify("fix bug in api", ctx)
    assert result.confidence > 0
