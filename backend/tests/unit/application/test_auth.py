import pytest
from uuid import uuid4

from reverse_todo.application.auth.use_cases import (
    LoginUserCommand,
    RegisterUserCommand,
    RegisterUserUseCase,
    LoginUserUseCase,
)
from reverse_todo.domain.errors import InvalidCredentialsError, UserAlreadyExistsError
from tests.fakes import FakeStore


@pytest.mark.asyncio
async def test_register_and_login():
    store = FakeStore()
    register = RegisterUserUseCase(store.users)
    login = LoginUserUseCase(store.users)
    user = await register.execute(
        RegisterUserCommand(email="a@b.com", password="password123")
    )
    assert user.email == "a@b.com"
    token, _ = await login.execute(LoginUserCommand(email="a@b.com", password="password123"))
    assert isinstance(token, str)
    assert len(token) > 10


@pytest.mark.asyncio
async def test_register_duplicate():
    store = FakeStore()
    register = RegisterUserUseCase(store.users)
    await register.execute(RegisterUserCommand(email="a@b.com", password="password123"))
    with pytest.raises(UserAlreadyExistsError):
        await register.execute(RegisterUserCommand(email="a@b.com", password="otherpass1"))


@pytest.mark.asyncio
async def test_login_invalid():
    store = FakeStore()
    login = LoginUserUseCase(store.users)
    with pytest.raises(InvalidCredentialsError):
        await login.execute(LoginUserCommand(email="x@y.com", password="wrongpass1"))
