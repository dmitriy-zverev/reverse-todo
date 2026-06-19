import re
from dataclasses import dataclass

from reverse_todo.domain.entities import ClassificationSuggestion
from reverse_todo.domain.ports.classification import ClassificationProvider, UserContext
from reverse_todo.domain.value_objects.category import TagCategory

MIN_SCORE = 1.0
TAG_BOOST = 2.0
PROJECT_BOOST = 1.5
SKILL_BOOST = 1.0

_TIE_BREAK: tuple[TagCategory, ...] = (
    TagCategory.LEARNING,
    TagCategory.HEALTH,
    TagCategory.HOME,
    TagCategory.RELATIONSHIPS,
    TagCategory.CREATIVE,
    TagCategory.FINANCE,
    TagCategory.INVISIBLE_WORK,
    TagCategory.WORK,
)


@dataclass(frozen=True, slots=True)
class KeywordRule:
    pattern: re.Pattern[str]
    category: TagCategory
    weight: float = 1.0


_KEYWORD_RULES: list[KeywordRule] = [
    KeywordRule(re.compile(r"\b(баг|bug|fix)\b", re.I), TagCategory.WORK, 1.5),
    KeywordRule(
        re.compile(r"\b(код[- ]?ревью|peer review|code review)\b", re.I),
        TagCategory.WORK,
        1.5,
    ),
    KeywordRule(
        re.compile(r"\b(api|docker|postgres|deploy|документац|sql)\b", re.I),
        TagCategory.WORK,
        1.0,
    ),
    KeywordRule(
        re.compile(r"\b(код|клиент|созвон|meeting|письмо|команд)\b", re.I),
        TagCategory.WORK,
        1.0,
    ),
    KeywordRule(re.compile(r"\b(починил|починить|написал)\b", re.I), TagCategory.WORK, 1.0),
    KeywordRule(
        re.compile(r"\b(прочитал|читал|learn|study|tutorial|практик|рефлекс)\b", re.I),
        TagCategory.LEARNING,
        1.5,
    ),
    KeywordRule(
        re.compile(r"\b(курс|course|глава|chapter|язык|language)\b", re.I),
        TagCategory.LEARNING,
        1.0,
    ),
    KeywordRule(
        re.compile(r"\b(прогул|погулял|трениров|gym|спорт|сон|sleep|медитац|отдых)\b", re.I),
        TagCategory.HEALTH,
        1.0,
    ),
    KeywordRule(re.compile(r"\b(уборк|готов|покупк|быт|почт)\b", re.I), TagCategory.HOME, 1.0),
    KeywordRule(
        re.compile(r"\b(позвонил|семь\w*|друг\w*|family|встрет\w*)\b", re.I),
        TagCategory.RELATIONSHIPS,
        1.0,
    ),
    KeywordRule(re.compile(r"\b(макет|design|рисов|paint|music)\b", re.I), TagCategory.CREATIVE, 1.0),
    KeywordRule(re.compile(r"\b(бюджет|finance|оплат|invoice|финанс)\b", re.I), TagCategory.FINANCE, 1.0),
    KeywordRule(
        re.compile(r"\b(поддержк|правк|редакт|дорог|commute|поиск)\b", re.I),
        TagCategory.INVISIBLE_WORK,
        1.0,
    ),
]


def _contains_term(text: str, term: str) -> bool:
    return bool(re.search(rf"\b{re.escape(term.lower())}\b", text, re.I))


def _score_keywords(text: str) -> dict[TagCategory, float]:
    scores: dict[TagCategory, float] = {}
    for rule in _KEYWORD_RULES:
        if rule.pattern.search(text):
            scores[rule.category] = scores.get(rule.category, 0.0) + rule.weight
    return scores


def _pick_category(scores: dict[TagCategory, float]) -> TagCategory | None:
    if not scores:
        return None
    max_score = max(scores.values())
    if max_score < MIN_SCORE:
        return None
    tied = [cat for cat, score in scores.items() if score == max_score]
    if len(tied) == 1:
        return tied[0]
    for cat in _TIE_BREAK:
        if cat in tied:
            return cat
    return tied[0]


def _confidence(max_score: float) -> float:
    if max_score < MIN_SCORE:
        return 0.25
    return min(0.95, 0.45 + 0.15 * max_score)


class RuleBasedClassifier(ClassificationProvider):
    async def classify(self, text: str, context: UserContext) -> ClassificationSuggestion:
        lowered = text.lower()
        scores = _score_keywords(lowered)

        for tag in context.tags:
            if _contains_term(lowered, tag.name):
                scores[tag.category] = scores.get(tag.category, 0.0) + TAG_BOOST

        project_name: str | None = None
        for project in sorted(context.projects, key=lambda p: len(p.name), reverse=True):
            if _contains_term(lowered, project.name):
                project_name = project.name
                scores[TagCategory.WORK] = scores.get(TagCategory.WORK, 0.0) + PROJECT_BOOST
                break

        skill_names: list[str] = []
        for skill in context.skills:
            if _contains_term(lowered, skill.name):
                skill_names.append(skill.name)
                scores[TagCategory.LEARNING] = scores.get(TagCategory.LEARNING, 0.0) + SKILL_BOOST

        max_score = max(scores.values()) if scores else 0.0
        category = _pick_category(scores)
        tag_names = (category.value,) if category is not None else ()

        return ClassificationSuggestion(
            tag_names=tag_names,
            category=category,
            project_name=project_name,
            skill_names=tuple(dict.fromkeys(skill_names)),
            confidence=_confidence(max_score),
        )


class LLMClassifierStub(ClassificationProvider):
    """Phase 2 placeholder — delegates to rules until LLM is wired."""

    def __init__(self) -> None:
        self._rules = RuleBasedClassifier()

    async def classify(self, text: str, context: UserContext) -> ClassificationSuggestion:
        return await self._rules.classify(text, context)
