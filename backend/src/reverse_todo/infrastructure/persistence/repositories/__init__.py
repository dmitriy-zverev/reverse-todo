from datetime import date
from uuid import UUID, uuid4

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from reverse_todo.domain.entities import Entry, Project, Skill, Tag
from reverse_todo.domain.value_objects.category import TagCategory
from reverse_todo.infrastructure.persistence.mappers import (
    entry_to_entity,
    project_to_entity,
    skill_to_entity,
    tag_to_entity,
)
from reverse_todo.infrastructure.persistence.models import (
    EntryModel,
    ProjectModel,
    SkillModel,
    TagModel,
)


class SqlAlchemyEntryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, entry: Entry) -> Entry:
        model = EntryModel(
            id=entry.id,
            user_id=entry.user_id,
            raw_text=entry.raw_text,
            entry_date=entry.entry_date,
            mood=entry.mood,
            energy=entry.energy,
            source=entry.source.value,
            project_id=entry.project_id,
            created_at=entry.created_at,
        )
        if entry.tags:
            tag_ids = [t.id for t in entry.tags]
            tags = (
                await self._session.scalars(select(TagModel).where(TagModel.id.in_(tag_ids)))
            ).all()
            model.tags = list(tags)
        if entry.skills:
            skill_ids = [s.id for s in entry.skills]
            skills = (
                await self._session.scalars(select(SkillModel).where(SkillModel.id.in_(skill_ids)))
            ).all()
            model.skills = list(skills)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model, ["tags", "skills"])
        return entry_to_entity(model)

    async def get_by_id(self, user_id: UUID, entry_id: UUID) -> Entry | None:
        stmt = (
            select(EntryModel)
            .where(EntryModel.id == entry_id, EntryModel.user_id == user_id)
            .options(selectinload(EntryModel.tags), selectinload(EntryModel.skills))
        )
        result = await self._session.scalar(stmt)
        return entry_to_entity(result) if result else None

    async def list_by_date_range(
        self, user_id: UUID, date_from: date, date_to: date
    ) -> list[Entry]:
        stmt = (
            select(EntryModel)
            .where(
                EntryModel.user_id == user_id,
                EntryModel.entry_date >= date_from,
                EntryModel.entry_date <= date_to,
            )
            .options(selectinload(EntryModel.tags), selectinload(EntryModel.skills))
            .order_by(EntryModel.created_at.desc())
        )
        rows = (await self._session.scalars(stmt)).all()
        return [entry_to_entity(r) for r in rows]

    async def list_by_user(self, user_id: UUID) -> list[Entry]:
        stmt = (
            select(EntryModel)
            .where(EntryModel.user_id == user_id)
            .options(selectinload(EntryModel.tags), selectinload(EntryModel.skills))
            .order_by(EntryModel.entry_date.desc(), EntryModel.created_at.desc())
        )
        rows = (await self._session.scalars(stmt)).all()
        return [entry_to_entity(r) for r in rows]

    async def update(self, entry: Entry) -> Entry:
        model = await self._session.get(
            EntryModel,
            entry.id,
            options=(selectinload(EntryModel.tags), selectinload(EntryModel.skills)),
        )
        if model is None:
            return entry
        model.project_id = entry.project_id
        model.mood = entry.mood
        model.energy = entry.energy
        tag_ids = [t.id for t in entry.tags]
        if tag_ids:
            tags = (
                await self._session.scalars(select(TagModel).where(TagModel.id.in_(tag_ids)))
            ).all()
            model.tags = list(tags)
        else:
            model.tags = []
        await self._session.flush()
        await self._session.refresh(model, ["tags", "skills"])
        return entry_to_entity(model)

    async def delete(self, user_id: UUID, entry_id: UUID) -> bool:
        stmt = delete(EntryModel).where(
            EntryModel.id == entry_id,
            EntryModel.user_id == user_id,
        )
        result = await self._session.execute(stmt)
        return result.rowcount > 0


class SqlAlchemyTagRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_user(self, user_id: UUID) -> list[Tag]:
        stmt = select(TagModel).where(TagModel.user_id == user_id)
        rows = (await self._session.scalars(stmt)).all()
        return [tag_to_entity(r) for r in rows]

    async def get_or_create(self, user_id: UUID, name: str, category: TagCategory) -> Tag:
        stmt = select(TagModel).where(TagModel.user_id == user_id, TagModel.name == name)
        existing = await self._session.scalar(stmt)
        if existing:
            return tag_to_entity(existing)
        model = TagModel(
            id=uuid4(), user_id=user_id, name=name, category=category.value
        )
        self._session.add(model)
        await self._session.flush()
        return tag_to_entity(model)


class SqlAlchemyProjectRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_user(self, user_id: UUID) -> list[Project]:
        stmt = select(ProjectModel).where(ProjectModel.user_id == user_id, ProjectModel.archived.is_(False))
        rows = (await self._session.scalars(stmt)).all()
        return [project_to_entity(r) for r in rows]

    async def get_or_create(self, user_id: UUID, name: str, color: str) -> Project:
        stmt = select(ProjectModel).where(ProjectModel.user_id == user_id, ProjectModel.name == name)
        existing = await self._session.scalar(stmt)
        if existing:
            return project_to_entity(existing)
        model = ProjectModel(id=uuid4(), user_id=user_id, name=name, color=color)
        self._session.add(model)
        await self._session.flush()
        return project_to_entity(model)

    async def create(self, project: Project) -> Project:
        model = ProjectModel(
            id=project.id,
            user_id=project.user_id,
            name=project.name,
            color=project.color,
            archived=project.archived,
        )
        self._session.add(model)
        await self._session.flush()
        return project_to_entity(model)


class SqlAlchemySkillRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_user(self, user_id: UUID) -> list[Skill]:
        stmt = select(SkillModel).where(SkillModel.user_id == user_id)
        rows = (await self._session.scalars(stmt)).all()
        return [skill_to_entity(r) for r in rows]

    async def get_or_create(self, user_id: UUID, name: str) -> Skill:
        stmt = select(SkillModel).where(SkillModel.user_id == user_id, SkillModel.name == name)
        existing = await self._session.scalar(stmt)
        if existing:
            return skill_to_entity(existing)
        model = SkillModel(id=uuid4(), user_id=user_id, name=name)
        self._session.add(model)
        await self._session.flush()
        return skill_to_entity(model)
