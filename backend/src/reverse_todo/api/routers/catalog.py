from fastapi import APIRouter, status

from reverse_todo.api.deps import CurrentUserDep
from reverse_todo.api.schemas import ProjectCreateRequest, ProjectResponse, TagResponse
from reverse_todo.infrastructure.di import SessionDep, UseCasesDep

router = APIRouter(tags=["catalog"])


@router.get("/projects", response_model=list[ProjectResponse])
async def list_projects(user: CurrentUserDep, use_cases: UseCasesDep) -> list[ProjectResponse]:
    projects = await use_cases.list_projects.execute(user.id)
    return [
        ProjectResponse(id=p.id, name=p.name, color=p.color, archived=p.archived) for p in projects
    ]


@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    body: ProjectCreateRequest,
    user: CurrentUserDep,
    use_cases: UseCasesDep,
    session: SessionDep,
) -> ProjectResponse:
    project = await use_cases.create_project.execute(user.id, body.name, body.color)
    await session.commit()
    return ProjectResponse(
        id=project.id, name=project.name, color=project.color, archived=project.archived
    )


@router.get("/tags", response_model=list[TagResponse])
async def list_tags(user: CurrentUserDep, use_cases: UseCasesDep) -> list[TagResponse]:
    tags = await use_cases.list_tags.execute(user.id)
    return [TagResponse(id=t.id, name=t.name, category=t.category) for t in tags]
