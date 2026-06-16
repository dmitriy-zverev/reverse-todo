from datetime import date, datetime
from uuid import uuid4

from reverse_todo.domain.value_objects.category import TagCategory
from reverse_todo.domain.value_objects.source import EntrySource
from reverse_todo.infrastructure.persistence.mappers import entry_to_entity, tag_to_entity
from reverse_todo.infrastructure.persistence.models import EntryModel, TagModel


def test_tag_mapper():
    model = TagModel(
        id=uuid4(),
        user_id=uuid4(),
        name="work",
        category=TagCategory.WORK.value,
    )
    entity = tag_to_entity(model)
    assert entity.name == "work"
    assert entity.category == TagCategory.WORK


def test_entry_mapper():
    model = EntryModel(
        id=uuid4(),
        user_id=uuid4(),
        raw_text="test",
        entry_date=date.today(),
        source=EntrySource.WEB.value,
        created_at=datetime.utcnow(),
        tags=[],
        skills=[],
    )
    entity = entry_to_entity(model)
    assert entity.raw_text == "test"
