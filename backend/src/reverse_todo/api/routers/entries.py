from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from reverse_todo.api.deps import CurrentUserDep
from reverse_todo.api.mappers import entry_to_response, suggestion_to_response
from reverse_todo.api.schemas import (
    CreateEntryRequest,
    CreateEntryResponse,
    EntryResponse,
    UpdateEntryRequest,
)
from reverse_todo.application.entries.create_entry import CreateEntryCommand
from reverse_todo.application.entries.delete_entry import DeleteEntryCommand
from reverse_todo.application.entries.update_entry import ListEntriesQuery, UpdateEntryCommand
from reverse_todo.domain.errors import EntryNotFoundError
from reverse_todo.domain.value_objects.source import EntrySource
from reverse_todo.infrastructure.di import SessionDep, UseCasesDep

router = APIRouter(prefix="/entries", tags=["entries"])


@router.post("", response_model=CreateEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_entry(
    body: CreateEntryRequest,
    user: CurrentUserDep,
    use_cases: UseCasesDep,
    session: SessionDep,
) -> CreateEntryResponse:
    entry, suggestion = await use_cases.create_entry.execute(
        CreateEntryCommand(
            user_id=user.id,
            timezone=user.timezone,
            raw_text=body.raw_text,
            source=EntrySource.WEB,
            entry_date=body.entry_date,
            mood=body.mood,
            energy=body.energy,
        )
    )
    await session.commit()
    return CreateEntryResponse(
        entry=entry_to_response(entry),
        suggestion=suggestion_to_response(suggestion),
    )


@router.get("", response_model=list[EntryResponse])
async def list_entries(
    user: CurrentUserDep,
    use_cases: UseCasesDep,
    date_from: Annotated[date | None, Query()] = None,
    date_to: Annotated[date | None, Query()] = None,
) -> list[EntryResponse]:
    entries = await use_cases.list_entries.execute(
        ListEntriesQuery(user_id=user.id, date_from=date_from, date_to=date_to)
    )
    return [entry_to_response(e) for e in entries]


@router.patch("/{entry_id}", response_model=EntryResponse)
async def update_entry(
    entry_id: UUID,
    body: UpdateEntryRequest,
    user: CurrentUserDep,
    use_cases: UseCasesDep,
    session: SessionDep,
) -> EntryResponse:
    try:
        entry = await use_cases.update_entry.execute(
            UpdateEntryCommand(
                user_id=user.id,
                entry_id=entry_id,
                project_id=body.project_id,
                tag_ids=body.tag_ids,
                category=body.category,
                mood=body.mood,
                update_mood="mood" in body.model_fields_set,
            )
        )
    except EntryNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    await session.commit()
    return entry_to_response(entry)


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entry(
    entry_id: UUID,
    user: CurrentUserDep,
    use_cases: UseCasesDep,
    session: SessionDep,
) -> None:
    try:
        await use_cases.delete_entry.execute(
            DeleteEntryCommand(user_id=user.id, entry_id=entry_id)
        )
    except EntryNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    await session.commit()
