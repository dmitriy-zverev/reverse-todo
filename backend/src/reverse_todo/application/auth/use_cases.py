from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from reverse_todo.domain.entities import User
from reverse_todo.domain.errors import InvalidCredentialsError, UserAlreadyExistsError
from reverse_todo.domain.repositories import UserRepository
from reverse_todo.infrastructure.auth.password import hash_password, verify_password
from reverse_todo.infrastructure.auth.tokens import create_access_token


@dataclass(slots=True)
class RegisterUserCommand:
    email: str
    password: str
    timezone: str = "UTC"


@dataclass(slots=True)
class LoginUserCommand:
    email: str
    password: str


class RegisterUserUseCase:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def execute(self, command: RegisterUserCommand) -> User:
        existing = await self._users.get_by_email(command.email.lower())
        if existing is not None:
            raise UserAlreadyExistsError("Email already registered")
        user = User(
            id=uuid4(),
            email=command.email.lower(),
            password_hash=hash_password(command.password),
            timezone=command.timezone,
            created_at=datetime.utcnow(),
        )
        return await self._users.create(user)


class LoginUserUseCase:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def execute(self, command: LoginUserCommand) -> tuple[str, User]:
        user = await self._users.get_by_email(command.email.lower())
        if user is None or not verify_password(command.password, user.password_hash):
            raise InvalidCredentialsError("Invalid email or password")
        return create_access_token(user.id), user
