from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from starlette.requests import Request

from reverse_todo.config import Settings, get_settings
from reverse_todo.domain.entities import User
from reverse_todo.infrastructure.auth.tokens import decode_access_token
from reverse_todo.infrastructure.di import SessionDep
from reverse_todo.infrastructure.persistence.repositories.user import SqlAlchemyUserRepository

SettingsDep = Annotated[Settings, Depends(get_settings)]


async def get_current_user_id(
    request: Request,
    settings: SettingsDep,
    session: SessionDep,
) -> UUID:
    token = request.cookies.get(settings.cookie_name)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")
    users = SqlAlchemyUserRepository(session)
    user = await users.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user_id


async def get_current_user(
    request: Request,
    settings: SettingsDep,
    session: SessionDep,
) -> User:
    user_id = await get_current_user_id(request, settings, session)
    users = SqlAlchemyUserRepository(session)
    user = await users.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


CurrentUserIdDep = Annotated[UUID, Depends(get_current_user_id)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
