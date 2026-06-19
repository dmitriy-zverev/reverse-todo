from uuid import uuid4

import pytest

from reverse_todo.application.classification.context import DefaultUserContext
from reverse_todo.domain.entities import Project, Tag
from reverse_todo.domain.value_objects.category import TagCategory
from reverse_todo.infrastructure.classification.rules import RuleBasedClassifier


@pytest.fixture
def classifier() -> RuleBasedClassifier:
    return RuleBasedClassifier()


@pytest.fixture
def empty_ctx() -> DefaultUserContext:
    return DefaultUserContext(user_id=uuid4(), timezone="UTC", projects=[], tags=[], skills=[])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected", "min_confidence"),
    [
        ("починил баг с авторизацией", TagCategory.WORK, 0.7),
        ("погулял 40 минут в парке", TagCategory.HEALTH, 0.0),
        ("прочитал главу про SQL", TagCategory.LEARNING, 0.0),
        ("код-ревью у коллеги", TagCategory.WORK, 0.0),
        ("разбирал SQL базу", TagCategory.WORK, 0.0),
        ("встретился с другом", TagCategory.RELATIONSHIPS, 0.0),
    ],
)
async def test_classifier_keyword_cases(
    classifier: RuleBasedClassifier,
    empty_ctx: DefaultUserContext,
    text: str,
    expected: TagCategory,
    min_confidence: float,
) -> None:
    result = await classifier.classify(text, empty_ctx)
    assert result.category == expected
    if min_confidence > 0:
        assert result.confidence >= min_confidence


@pytest.mark.asyncio
async def test_classifier_abstains_on_ambiguous(
    classifier: RuleBasedClassifier, empty_ctx: DefaultUserContext
) -> None:
    result = await classifier.classify("ничего особенного", empty_ctx)
    assert result.category is None
    assert result.confidence <= 0.3
    assert result.tag_names == ()


@pytest.mark.asyncio
async def test_classifier_user_tag_boost(classifier: RuleBasedClassifier) -> None:
    user_id = uuid4()
    ctx = DefaultUserContext(
        user_id=user_id,
        timezone="UTC",
        projects=[],
        tags=[
            Tag(id=uuid4(), user_id=user_id, name="прогулка", category=TagCategory.HEALTH),
        ],
        skills=[],
    )
    result = await classifier.classify("вечерняя прогулка", ctx)
    assert result.category == TagCategory.HEALTH


@pytest.mark.asyncio
async def test_classifier_project_word_boundary(classifier: RuleBasedClassifier) -> None:
    user_id = uuid4()
    ctx = DefaultUserContext(
        user_id=user_id,
        timezone="UTC",
        projects=[
            Project(id=uuid4(), user_id=user_id, name="Auth", color="#000", archived=False),
        ],
        tags=[],
        skills=[],
    )
    result = await classifier.classify("author said hi", ctx)
    assert result.project_name is None


@pytest.mark.asyncio
async def test_classifier_code_review_not_invisible(
    classifier: RuleBasedClassifier, empty_ctx: DefaultUserContext
) -> None:
    result = await classifier.classify("код-ревью у коллеги", empty_ctx)
    assert result.category == TagCategory.WORK
    assert result.category != TagCategory.INVISIBLE_WORK


@pytest.mark.asyncio
async def test_classifier_learning_beats_sql_work_token(
    classifier: RuleBasedClassifier, empty_ctx: DefaultUserContext
) -> None:
    result = await classifier.classify("прочитал главу про SQL", empty_ctx)
    assert result.category == TagCategory.LEARNING
