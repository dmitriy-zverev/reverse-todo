from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from reverse_todo.application.auth.use_cases import LoginUserUseCase, RegisterUserUseCase
from reverse_todo.application.catalog.use_cases import (
    CreateProjectUseCase,
    ListProjectsUseCase,
    ListTagsUseCase,
)
from reverse_todo.application.entries.create_entry import CreateEntryUseCase
from reverse_todo.application.entries.delete_entry import DeleteEntryUseCase
from reverse_todo.application.entries.update_entry import ListEntriesUseCase, UpdateEntryUseCase
from reverse_todo.application.reports.today import GetTodaySummaryUseCase
from reverse_todo.application.reports.weekly import GetWeeklyReportUseCase
from reverse_todo.config import Settings, get_settings
from reverse_todo.domain.ports.classification import ClassificationProvider
from reverse_todo.infrastructure.classification.llm import LLMClassifierStub
from reverse_todo.infrastructure.classification.rules import RuleBasedClassifier
from reverse_todo.infrastructure.persistence.database import get_session
from reverse_todo.infrastructure.persistence.repositories import (
    SqlAlchemyEntryRepository,
    SqlAlchemyProjectRepository,
    SqlAlchemySkillRepository,
    SqlAlchemyTagRepository,
)
from reverse_todo.infrastructure.persistence.repositories.user import SqlAlchemyUserRepository


@dataclass(slots=True)
class UseCases:
    create_entry: CreateEntryUseCase
    update_entry: UpdateEntryUseCase
    delete_entry: DeleteEntryUseCase
    list_entries: ListEntriesUseCase
    weekly_report: GetWeeklyReportUseCase
    today_summary: GetTodaySummaryUseCase
    register_user: RegisterUserUseCase
    login_user: LoginUserUseCase
    list_projects: ListProjectsUseCase
    create_project: CreateProjectUseCase
    list_tags: ListTagsUseCase


def get_classifier(settings: Annotated[Settings, Depends(get_settings)]) -> ClassificationProvider:
    if settings.classifier_backend == "llm":
        return LLMClassifierStub()
    return RuleBasedClassifier()


async def get_use_cases(
    session: Annotated[AsyncSession, Depends(get_session)],
    classifier: Annotated[ClassificationProvider, Depends(get_classifier)],
) -> UseCases:
    entries = SqlAlchemyEntryRepository(session)
    tags = SqlAlchemyTagRepository(session)
    projects = SqlAlchemyProjectRepository(session)
    skills = SqlAlchemySkillRepository(session)
    users = SqlAlchemyUserRepository(session)
    return UseCases(
        create_entry=CreateEntryUseCase(entries, tags, projects, skills, classifier),
        update_entry=UpdateEntryUseCase(entries, tags),
        delete_entry=DeleteEntryUseCase(entries),
        list_entries=ListEntriesUseCase(entries),
        weekly_report=GetWeeklyReportUseCase(entries, projects),
        today_summary=GetTodaySummaryUseCase(entries),
        register_user=RegisterUserUseCase(users),
        login_user=LoginUserUseCase(users),
        list_projects=ListProjectsUseCase(projects),
        create_project=CreateProjectUseCase(projects),
        list_tags=ListTagsUseCase(tags),
    )


UseCasesDep = Annotated[UseCases, Depends(get_use_cases)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
