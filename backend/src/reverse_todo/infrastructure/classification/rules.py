import re
from uuid import uuid4

from reverse_todo.application.classification.context import DefaultUserContext
from reverse_todo.domain.entities import ClassificationSuggestion
from reverse_todo.domain.ports.classification import ClassificationProvider, UserContext
from reverse_todo.domain.value_objects.category import TagCategory

_KEYWORD_RULES: list[tuple[re.Pattern[str], TagCategory, str]] = [
    (re.compile(r"\b(баг|bug|fix|api|docker|postgres|sql|код|deploy|клиент|созвон|meeting)\b", re.I), TagCategory.WORK, "work"),
    (re.compile(r"\b(читал|learn|курс|course|глава|study|tutorial)\b", re.I), TagCategory.LEARNING, "learning"),
    (re.compile(r"\b(прогул|погулял|gym|спорт|сон|sleep|медитац)\b", re.I), TagCategory.HEALTH, "health"),
    (re.compile(r"\b(уборк|готовил|документ|быт)\b", re.I), TagCategory.HOME, "home"),
    (re.compile(r"\b(позвонил|семь|друг|family|call)\b", re.I), TagCategory.RELATIONSHIPS, "relationships"),
    (re.compile(r"\b(макет|design|рисов|paint|music)\b", re.I), TagCategory.CREATIVE, "creative"),
    (re.compile(r"\b(бюджет|finance|оплат|invoice)\b", re.I), TagCategory.FINANCE, "finance"),
    (re.compile(r"\b(поддержк|review|правк|дорог|commute|поиск)\b", re.I), TagCategory.INVISIBLE_WORK, "invisible"),
]


class RuleBasedClassifier(ClassificationProvider):
    async def classify(self, text: str, context: UserContext) -> ClassificationSuggestion:
        lowered = text.lower()
        category: TagCategory | None = None
        tag_names: list[str] = []
        confidence = 0.3

        for pattern, cat, tag in _KEYWORD_RULES:
            if pattern.search(lowered):
                category = cat
                tag_names.append(tag)
                confidence = 0.75
                break

        project_name: str | None = None
        for project in context.projects:
            if project.name.lower() in lowered:
                project_name = project.name
                confidence = max(confidence, 0.85)
                break

        skill_names: list[str] = []
        for skill in context.skills:
            if skill.name.lower() in lowered:
                skill_names.append(skill.name)
                confidence = max(confidence, 0.8)

        if category is None and not tag_names:
            tag_names = ["general"]
            confidence = 0.25

        return ClassificationSuggestion(
            tag_names=tuple(dict.fromkeys(tag_names)),
            category=category,
            project_name=project_name,
            skill_names=tuple(skill_names),
            confidence=confidence,
        )


class LLMClassifierStub(ClassificationProvider):
    """Phase 2 placeholder — delegates to rules until LLM is wired."""

    def __init__(self) -> None:
        self._rules = RuleBasedClassifier()

    async def classify(self, text: str, context: UserContext) -> ClassificationSuggestion:
        return await self._rules.classify(text, context)
