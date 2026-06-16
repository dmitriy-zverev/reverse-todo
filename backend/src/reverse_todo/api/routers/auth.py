from fastapi import APIRouter, HTTPException, Response, status

from reverse_todo.api.deps import CurrentUserDep, SettingsDep
from reverse_todo.api.schemas import LoginRequest, RegisterRequest, UserResponse
from reverse_todo.application.auth.use_cases import LoginUserCommand, RegisterUserCommand
from reverse_todo.domain.errors import InvalidCredentialsError, UserAlreadyExistsError
from reverse_todo.infrastructure.di import SessionDep, UseCasesDep


router = APIRouter(prefix="/auth", tags=["auth"])


def _set_session_cookie(response: Response, settings: SettingsDep, token: str) -> None:
    response.set_cookie(
        key=settings.cookie_name,
        value=token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        max_age=settings.access_token_expire_minutes * 60,
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    body: RegisterRequest,
    response: Response,
    use_cases: UseCasesDep,
    settings: SettingsDep,
    session: SessionDep,
) -> UserResponse:
    try:
        user = await use_cases.register_user.execute(
            RegisterUserCommand(email=body.email, password=body.password, timezone=body.timezone)
        )
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    await session.commit()
    token, _ = await use_cases.login_user.execute(
        LoginUserCommand(email=body.email, password=body.password)
    )
    _set_session_cookie(response, settings, token)
    return UserResponse(id=user.id, email=user.email, timezone=user.timezone)


@router.post("/login", response_model=UserResponse)
async def login(
    body: LoginRequest,
    response: Response,
    use_cases: UseCasesDep,
    settings: SettingsDep,
    session: SessionDep,
) -> UserResponse:
    try:
        token, user = await use_cases.login_user.execute(
            LoginUserCommand(email=body.email, password=body.password)
        )
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    _set_session_cookie(response, settings, token)
    return UserResponse(id=user.id, email=user.email, timezone=user.timezone)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response, settings: SettingsDep) -> None:
    response.delete_cookie(key=settings.cookie_name)


@router.get("/me", response_model=UserResponse)
async def me(user: CurrentUserDep) -> UserResponse:
    return UserResponse(id=user.id, email=user.email, timezone=user.timezone)
