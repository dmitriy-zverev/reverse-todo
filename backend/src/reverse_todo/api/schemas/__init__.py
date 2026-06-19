from datetime import date, datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from reverse_todo.domain.value_objects.category import TagCategory


class RegisterRequest(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8, max_length=128)]
    timezone: str = "UTC"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    timezone: str | None = None


class UserResponse(BaseModel):
    id: UUID
    email: str
    timezone: str


class TagResponse(BaseModel):
    id: UUID
    name: str
    category: TagCategory


class SkillResponse(BaseModel):
    id: UUID
    name: str


class EntryResponse(BaseModel):
    id: UUID
    raw_text: str
    entry_date: date
    source: str
    mood: int | None
    energy: int | None
    project_id: UUID | None
    tags: list[TagResponse]
    skills: list[SkillResponse]
    created_at: datetime


class ClassificationResponse(BaseModel):
    tag_names: list[str]
    category: TagCategory | None
    project_name: str | None
    skill_names: list[str]
    confidence: float


class CreateEntryRequest(BaseModel):
    raw_text: Annotated[str, Field(min_length=1, max_length=2000)]
    entry_date: date | None = None
    mood: Annotated[int | None, Field(ge=1, le=5)] = None
    energy: Annotated[int | None, Field(ge=1, le=5)] = None


class CreateEntryResponse(BaseModel):
    entry: EntryResponse
    suggestion: ClassificationResponse


class UpdateEntryRequest(BaseModel):
    project_id: UUID | None = None
    tag_ids: list[UUID] | None = None
    category: TagCategory | None = None
    mood: Annotated[int | None, Field(ge=1, le=5)] = None


class CategoryCountResponse(BaseModel):
    category: TagCategory
    count: int


class ProjectCountResponse(BaseModel):
    project_id: UUID
    project_name: str
    count: int


class StreakResponse(BaseModel):
    label: str
    days: int


class WeeklyReportResponse(BaseModel):
    week_start: date
    week_end: date
    total_entries: int
    daily_counts: list[int]
    category_counts: list[CategoryCountResponse]
    top_project: ProjectCountResponse | None
    streaks: list[StreakResponse]
    invisible_work_count: int
    narrative: str


class TodaySummaryResponse(BaseModel):
    entry_date: date
    entry_count: int
    entries: list[EntryResponse]


class ProjectCreateRequest(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=120)]
    color: str = "#64748b"


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    color: str
    archived: bool
