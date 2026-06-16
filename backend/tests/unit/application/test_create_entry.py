from datetime import date, datetime, timedelta
from uuid import uuid4

import pytest

from reverse_todo.application.entries.create_entry import CreateEntryCommand, CreateEntryUseCase
from reverse_todo.application.reports.weekly import GetWeeklyReportQuery, GetWeeklyReportUseCase
from reverse_todo.domain.entities import Project
from reverse_todo.domain.value_objects.category import TagCategory
from reverse_todo.domain.value_objects.source import EntrySource
from reverse_todo.infrastructure.classification.rules import RuleBasedClassifier
from tests.fakes import FakeStore


@pytest.fixture
def store() -> FakeStore:
    return FakeStore()


@pytest.fixture
def create_use_case(store: FakeStore) -> CreateEntryUseCase:
    return CreateEntryUseCase(
        store.entries,
        store.tags,
        store.projects,
        store.skills,
        RuleBasedClassifier(),
    )


@pytest.mark.asyncio
async def test_create_entry_classifies_work(store: FakeStore, create_use_case: CreateEntryUseCase):
    user_id = uuid4()
    store.projects.projects[uuid4()] = Project(
        id=uuid4(), user_id=user_id, name="Auth", color="#000", archived=False
    )
    entry, suggestion = await create_use_case.execute(
        CreateEntryCommand(
            user_id=user_id,
            timezone="UTC",
            raw_text="починил баг с авторизацией",
            source=EntrySource.WEB,
        )
    )
    assert entry.raw_text == "починил баг с авторизацией"
    assert suggestion.category == TagCategory.WORK
    assert suggestion.confidence >= 0.7
    assert len(entry.tags) >= 1


@pytest.mark.asyncio
async def test_create_entry_scoped_by_user(store: FakeStore, create_use_case: CreateEntryUseCase):
    user_a, user_b = uuid4(), uuid4()
    entry, _ = await create_use_case.execute(
        CreateEntryCommand(
            user_id=user_a,
            timezone="UTC",
            raw_text="прочитал главу",
            source=EntrySource.WEB,
        )
    )
    assert await store.entries.get_by_id(user_b, entry.id) is None
    assert await store.entries.get_by_id(user_a, entry.id) is not None


@pytest.mark.asyncio
async def test_weekly_report_streak(store: FakeStore):
    user_id = uuid4()
    classifier = RuleBasedClassifier()
    uc = CreateEntryUseCase(
        store.entries, store.tags, store.projects, store.skills, classifier
    )
    week_start = date(2025, 6, 9)
    for offset in range(3):
        await uc.execute(
            CreateEntryCommand(
                user_id=user_id,
                timezone="UTC",
                raw_text="разбирал SQL базу",
                source=EntrySource.WEB,
                entry_date=week_start + timedelta(days=offset),
            )
        )
    report_uc = GetWeeklyReportUseCase(store.entries, store.projects)
    report = await report_uc.execute(GetWeeklyReportQuery(user_id=user_id, week_start=week_start))
    assert report.total_entries == 3
    assert report.daily_counts == (1, 1, 1, 0, 0, 0, 0)
    assert report.category_counts[0].category == TagCategory.WORK
    assert any(s.days >= 3 for s in report.streaks)


@pytest.mark.asyncio
async def test_weekly_empty(store: FakeStore):
    report = await GetWeeklyReportUseCase(store.entries, store.projects).execute(
        GetWeeklyReportQuery(user_id=uuid4(), week_start=date(2025, 1, 6))
    )
    assert report.total_entries == 0
    assert report.daily_counts == (0, 0, 0, 0, 0, 0, 0)
    assert report.invisible_work_count == 0


@pytest.mark.asyncio
async def test_classifier_russian_health():
    from reverse_todo.application.classification.context import DefaultUserContext

    classifier = RuleBasedClassifier()
    ctx = DefaultUserContext(user_id=uuid4(), timezone="UTC", projects=[], tags=[], skills=[])
    result = await classifier.classify("погулял 40 минут в парке", ctx)
    assert result.category == TagCategory.HEALTH


@pytest.mark.asyncio
async def test_entry_date_timezone():
    from reverse_todo.domain.value_objects.entry_date import EntryDate

    with __import__("time_machine").travel("2025-06-15 23:00:00", tick=False):
        d = EntryDate.today_in_timezone("Europe/Moscow")
    assert isinstance(d.value, date)
