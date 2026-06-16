from uuid import UUID, uuid4

from reverse_todo.domain.entities import Project
from reverse_todo.domain.repositories import ProjectRepository, TagRepository


class ListProjectsUseCase:
    def __init__(self, projects: ProjectRepository) -> None:
        self._projects = projects

    async def execute(self, user_id: UUID) -> list[Project]:
        return await self._projects.list_by_user(user_id)


class CreateProjectUseCase:
    def __init__(self, projects: ProjectRepository) -> None:
        self._projects = projects

    async def execute(self, user_id: UUID, name: str, color: str) -> Project:
        return await self._projects.create(
            Project(id=uuid4(), user_id=user_id, name=name, color=color, archived=False)
        )


class ListTagsUseCase:
    def __init__(self, tags: TagRepository) -> None:
        self._tags = tags

    async def execute(self, user_id: UUID):
        return await self._tags.list_by_user(user_id)
