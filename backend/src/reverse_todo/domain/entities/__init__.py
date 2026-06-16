from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID

from reverse_todo.domain.value_objects.category import TagCategory
from reverse_todo.domain.value_objects.source import EntrySource


@dataclass(slots=True)
class User:
    id: UUID
    email: str
    password_hash: str
    timezone: str
    created_at: datetime


@dataclass(slots=True)
class Tag:
    id: UUID
    user_id: UUID
    name: str
    category: TagCategory


@dataclass(slots=True)
class Skill:
    id: UUID
    user_id: UUID
    name: str


@dataclass(slots=True)
class Project:
    id: UUID
    user_id: UUID
    name: str
    color: str
    archived: bool = False


@dataclass(slots=True)
class Entry:
    id: UUID
    user_id: UUID
    raw_text: str
    entry_date: date
    source: EntrySource
    created_at: datetime
    mood: int | None = None
    energy: int | None = None
    project_id: UUID | None = None
    tags: list[Tag] = field(default_factory=list)
    skills: list[Skill] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class ClassificationSuggestion:
    tag_names: tuple[str, ...]
    category: TagCategory | None
    project_name: str | None
    skill_names: tuple[str, ...]
    confidence: float


@dataclass(frozen=True, slots=True)
class CategoryCount:
    category: TagCategory
    count: int


@dataclass(frozen=True, slots=True)
class ProjectCount:
    project_id: UUID
    project_name: str
    count: int


@dataclass(frozen=True, slots=True)
class StreakInsight:
    label: str
    days: int


@dataclass(frozen=True, slots=True)
class WeeklyReport:
    week_start: date
    week_end: date
    total_entries: int
    daily_counts: tuple[int, ...]
    category_counts: tuple[CategoryCount, ...]
    top_project: ProjectCount | None
    streaks: tuple[StreakInsight, ...]
    invisible_work_count: int
    narrative: str


@dataclass(frozen=True, slots=True)
class TodaySummary:
    entry_date: date
    entry_count: int
    entries: tuple[Entry, ...]
