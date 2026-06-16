from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from reverse_todo.domain.entities import User
from reverse_todo.infrastructure.persistence.mappers import user_to_entity
from reverse_todo.infrastructure.persistence.models import UserModel


class SqlAlchemyUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self._session.get(UserModel, user_id)
        return user_to_entity(result) if result else None

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self._session.scalar(stmt)
        return user_to_entity(result) if result else None

    async def create(self, user: User) -> User:
        model = UserModel(
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
            timezone=user.timezone,
            created_at=user.created_at,
        )
        self._session.add(model)
        await self._session.flush()
        return user_to_entity(model)
