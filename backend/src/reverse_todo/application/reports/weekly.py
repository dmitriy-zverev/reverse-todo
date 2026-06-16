from dataclasses import dataclass
from datetime import date, timedelta
from uuid import UUID

from reverse_todo.domain.entities import (
    CategoryCount,
    ProjectCount,
    StreakInsight,
    WeeklyReport,
)
from reverse_todo.domain.repositories import EntryRepository, ProjectRepository
from reverse_todo.domain.value_objects.category import TagCategory

_CATEGORY_RU: dict[TagCategory, str] = {
    TagCategory.WORK: "работа",
    TagCategory.LEARNING: "обучение",
    TagCategory.HEALTH: "здоровье",
    TagCategory.HOME: "дом",
    TagCategory.RELATIONSHIPS: "отношения",
    TagCategory.CREATIVE: "творчество",
    TagCategory.FINANCE: "финансы",
    TagCategory.INVISIBLE_WORK: "невидимая работа",
}


@dataclass(slots=True)
class GetWeeklyReportQuery:
    user_id: UUID
    week_start: date


class GetWeeklyReportUseCase:
    def __init__(
        self,
        entries: EntryRepository,
        projects: ProjectRepository,
    ) -> None:
        self._entries = entries
        self._projects = projects

    async def execute(self, query: GetWeeklyReportQuery) -> WeeklyReport:
        week_start = query.week_start
        week_end = week_start + timedelta(days=6)
        items = await self._entries.list_by_date_range(query.user_id, week_start, week_end)
        project_names = {p.id: p.name for p in await self._projects.list_by_user(query.user_id)}

        category_map: dict[TagCategory, int] = {}
        project_counts: dict[UUID, int] = {}
        invisible = 0
        tag_days: dict[str, set[date]] = {}
        daily_map: dict[date, int] = {}

        for entry in items:
            daily_map[entry.entry_date] = daily_map.get(entry.entry_date, 0) + 1
            if entry.project_id:
                project_counts[entry.project_id] = project_counts.get(entry.project_id, 0) + 1
            for tag in entry.tags:
                category_map[tag.category] = category_map.get(tag.category, 0) + 1
                if tag.category == TagCategory.INVISIBLE_WORK:
                    invisible += 1
                tag_days.setdefault(tag.name, set()).add(entry.entry_date)

        category_counts = tuple(
            CategoryCount(category=c, count=n)
            for c, n in sorted(category_map.items(), key=lambda x: -x[1])
        )

        top_project = None
        if project_counts:
            best_id = max(project_counts, key=project_counts.get)  # type: ignore[arg-type]
            top_project = ProjectCount(
                project_id=best_id,
                project_name=project_names.get(best_id, "Unknown"),
                count=project_counts[best_id],
            )

        streaks = tuple(
            StreakInsight(label=label, days=streak)
            for label, days_set in tag_days.items()
            if (streak := _longest_streak(days_set, week_start, week_end)) >= 3
        )

        total = len(items)
        lead = (
            _CATEGORY_RU.get(category_counts[0].category, category_counts[0].category.value)
            if category_counts
            else "—"
        )
        narrative = f"На этой неделе {total} записей. Больше всего — {lead}."
        daily_counts = tuple(
            daily_map.get(week_start + timedelta(days=offset), 0) for offset in range(7)
        )

        return WeeklyReport(
            week_start=week_start,
            week_end=week_end,
            total_entries=total,
            daily_counts=daily_counts,
            category_counts=category_counts,
            top_project=top_project,
            streaks=streaks,
            invisible_work_count=invisible,
            narrative=narrative,
        )


def _longest_streak(days: set[date], start: date, end: date) -> int:
    best = 0
    current = 0
    d = start
    while d <= end:
        if d in days:
            current += 1
            best = max(best, current)
        else:
            current = 0
        d += timedelta(days=1)
    return best
