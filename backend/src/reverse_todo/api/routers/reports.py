from datetime import date, timedelta
from typing import Annotated

from fastapi import APIRouter, Query

from reverse_todo.api.deps import CurrentUserDep
from reverse_todo.api.mappers import entry_to_response
from reverse_todo.api.schemas import (
    CategoryCountResponse,
    ProjectCountResponse,
    StreakResponse,
    TodaySummaryResponse,
    WeeklyReportResponse,
)
from reverse_todo.application.reports.weekly import GetWeeklyReportQuery
from reverse_todo.domain.value_objects.entry_date import EntryDate
from reverse_todo.infrastructure.di import UseCasesDep

router = APIRouter(prefix="/reports", tags=["reports"])


def _week_start(d: date) -> date:
    return d - timedelta(days=d.weekday())


@router.get("/weekly", response_model=WeeklyReportResponse)
async def weekly_report(
    user: CurrentUserDep,
    use_cases: UseCasesDep,
    week: Annotated[date | None, Query()] = None,
) -> WeeklyReportResponse:
    week_start = _week_start(week or EntryDate.today_in_timezone(user.timezone).value)
    report = await use_cases.weekly_report.execute(
        GetWeeklyReportQuery(user_id=user.id, week_start=week_start)
    )
    return WeeklyReportResponse(
        week_start=report.week_start,
        week_end=report.week_end,
        total_entries=report.total_entries,
        daily_counts=list(report.daily_counts),
        category_counts=[
            CategoryCountResponse(category=c.category, count=c.count)
            for c in report.category_counts
        ],
        top_project=(
            ProjectCountResponse(
                project_id=report.top_project.project_id,
                project_name=report.top_project.project_name,
                count=report.top_project.count,
            )
            if report.top_project
            else None
        ),
        streaks=[StreakResponse(label=s.label, days=s.days) for s in report.streaks],
        invisible_work_count=report.invisible_work_count,
        narrative=report.narrative,
    )


@router.get("/today", response_model=TodaySummaryResponse)
async def today_report(user: CurrentUserDep, use_cases: UseCasesDep) -> TodaySummaryResponse:
    summary = await use_cases.today_summary.execute(user.id, user.timezone)
    return TodaySummaryResponse(
        entry_date=summary.entry_date,
        entry_count=summary.entry_count,
        entries=[entry_to_response(e) for e in summary.entries],
    )
