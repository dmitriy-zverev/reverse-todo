from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID, uuid4

from reverse_todo.application.classification.context import DefaultUserContext
from reverse_todo.domain.entities import Entry
from reverse_todo.domain.ports.classification import ClassificationProvider
from reverse_todo.domain.repositories import (
    EntryRepository,
    ProjectRepository,
    SkillRepository,
    TagRepository,
)
from reverse_todo.domain.value_objects.entry_date import EntryDate
from reverse_todo.domain.value_objects.source import EntrySource


@dataclass(slots=True)
class CreateEntryCommand:
    user_id: UUID
    timezone: str
    raw_text: str
    source: EntrySource
    entry_date: date | None = None
    mood: int | None = None
    energy: int | None = None


class CreateEntryUseCase:
    def __init__(
        self,
        entries: EntryRepository,
        tags: TagRepository,
        projects: ProjectRepository,
        skills: SkillRepository,
        classifier: ClassificationProvider,
    ) -> None:
        self._entries = entries
        self._tags = tags
        self._projects = projects
        self._skills = skills
        self._classifier = classifier

    async def execute(self, command: CreateEntryCommand) -> tuple[Entry, object]:
        entry_date = EntryDate.from_optional(command.entry_date, command.timezone)
        projects = await self._projects.list_by_user(command.user_id)
        tag_list = await self._tags.list_by_user(command.user_id)
        skill_list = await self._skills.list_by_user(command.user_id)
        context = DefaultUserContext(
            user_id=command.user_id,
            timezone=command.timezone,
            projects=projects,
            tags=tag_list,
            skills=skill_list,
        )
        suggestion = await self._classifier.classify(command.raw_text, context)

        entry = Entry(
            id=uuid4(),
            user_id=command.user_id,
            raw_text=command.raw_text.strip(),
            entry_date=entry_date.value,
            source=command.source,
            created_at=datetime.utcnow(),
            mood=command.mood,
            energy=command.energy,
        )

        linked_tags = []
        if suggestion.category is not None:
            for name in suggestion.tag_names:
                linked_tags.append(
                    await self._tags.get_or_create(command.user_id, name, suggestion.category)
                )
        entry.tags = linked_tags

        if suggestion.project_name:
            project = await self._projects.get_or_create(
                command.user_id, suggestion.project_name, "#64748b"
            )
            entry.project_id = project.id

        linked_skills = []
        for name in suggestion.skill_names:
            linked_skills.append(await self._skills.get_or_create(command.user_id, name))
        entry.skills = linked_skills

        saved = await self._entries.create(entry)
        return saved, suggestion
