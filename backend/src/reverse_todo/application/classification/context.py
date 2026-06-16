from dataclasses import dataclass
from uuid import UUID

from reverse_todo.domain.entities import Project, Skill, Tag


@dataclass(frozen=True, slots=True)
class DefaultUserContext:
    user_id: UUID
    timezone: str
    projects: list[Project]
    tags: list[Tag]
    skills: list[Skill]
