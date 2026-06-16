from reverse_todo.domain.entities import Entry
from reverse_todo.api.schemas import (
    ClassificationResponse,
    EntryResponse,
    SkillResponse,
    TagResponse,
)


def entry_to_response(entry: Entry) -> EntryResponse:
    return EntryResponse(
        id=entry.id,
        raw_text=entry.raw_text,
        entry_date=entry.entry_date,
        source=entry.source.value,
        mood=entry.mood,
        energy=entry.energy,
        project_id=entry.project_id,
        tags=[TagResponse(id=t.id, name=t.name, category=t.category) for t in entry.tags],
        skills=[SkillResponse(id=s.id, name=s.name) for s in entry.skills],
        created_at=entry.created_at,
    )


def suggestion_to_response(suggestion: object) -> ClassificationResponse:
    return ClassificationResponse(
        tag_names=list(suggestion.tag_names),
        category=suggestion.category,
        project_name=suggestion.project_name,
        skill_names=list(suggestion.skill_names),
        confidence=suggestion.confidence,
    )
