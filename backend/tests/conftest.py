import os
from collections.abc import AsyncGenerator
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

os.environ.setdefault(
    "SECRET_KEY",
    "test-secret-key-minimum-32-characters-long",
)
os.environ.setdefault(
    "DATABASE_URL",
    "sqlite+aiosqlite:///:memory:",
)

from reverse_todo.api.deps import get_current_user, get_current_user_id
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
from reverse_todo.config import get_settings
from reverse_todo.domain.entities import User
from reverse_todo.infrastructure.auth.tokens import decode_access_token
from reverse_todo.infrastructure.classification.rules import RuleBasedClassifier
from reverse_todo.infrastructure.di import UseCases, get_use_cases
from reverse_todo.infrastructure.persistence.database import get_session
from reverse_todo.main import create_app
from starlette.requests import Request
from tests.fakes import FakeStore


@pytest.fixture
def fake_store() -> FakeStore:
    return FakeStore()


@pytest.fixture
def use_cases(fake_store: FakeStore) -> UseCases:
    classifier = RuleBasedClassifier()
    return UseCases(
        create_entry=CreateEntryUseCase(
            fake_store.entries,
            fake_store.tags,
            fake_store.projects,
            fake_store.skills,
            classifier,
        ),
        update_entry=UpdateEntryUseCase(fake_store.entries, fake_store.tags),
        delete_entry=DeleteEntryUseCase(fake_store.entries),
        list_entries=ListEntriesUseCase(fake_store.entries),
        weekly_report=GetWeeklyReportUseCase(fake_store.entries, fake_store.projects),
        today_summary=GetTodaySummaryUseCase(fake_store.entries),
        register_user=RegisterUserUseCase(fake_store.users),
        login_user=LoginUserUseCase(fake_store.users),
        list_projects=ListProjectsUseCase(fake_store.projects),
        create_project=CreateProjectUseCase(fake_store.projects),
        list_tags=ListTagsUseCase(fake_store.tags),
    )


class _NullSession:
    async def commit(self) -> None:
        return None

    async def flush(self) -> None:
        return None


@pytest.fixture
async def app(fake_store: FakeStore, use_cases: UseCases):
    application = create_app()

    async def override_use_cases() -> UseCases:
        return use_cases

    async def override_session() -> AsyncGenerator[_NullSession, None]:
        yield _NullSession()

    async def override_get_current_user_id(request: Request) -> UUID:
        settings = get_settings()
        token = request.cookies.get(settings.cookie_name)
        user_id = decode_access_token(token or "")
        if user_id is None:
            from fastapi import HTTPException, status

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return user_id

    async def override_get_current_user(request: Request) -> User:
        user_id = await override_get_current_user_id(request)
        user = fake_store.users.users.get(user_id)
        if user is None:
            from fastapi import HTTPException, status

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return user

    application.dependency_overrides[get_use_cases] = override_use_cases
    application.dependency_overrides[get_session] = override_session
    application.dependency_overrides[get_current_user_id] = override_get_current_user_id
    application.dependency_overrides[get_current_user] = override_get_current_user
    get_settings.cache_clear()
    yield application
    application.dependency_overrides.clear()
    get_settings.cache_clear()


@pytest.fixture
async def client(app) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def auth_client(client: AsyncClient) -> AsyncGenerator[tuple[AsyncClient, UUID], None]:
    response = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123", "timezone": "UTC"},
    )
    assert response.status_code == 201
    user_id = UUID(response.json()["id"])
    yield client, user_id
