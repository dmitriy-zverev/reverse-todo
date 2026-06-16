from reverse_todo.domain.entities import Entry, Project, Skill, Tag, User
from reverse_todo.domain.value_objects.category import TagCategory
from reverse_todo.domain.value_objects.source import EntrySource
from reverse_todo.infrastructure.persistence.models import (
    EntryModel,
    ProjectModel,
    SkillModel,
    TagModel,
    UserModel,
)


def user_to_entity(model: UserModel) -> User:
    return User(
        id=model.id,
        email=model.email,
        password_hash=model.password_hash,
        timezone=model.timezone,
        created_at=model.created_at,
    )


def tag_to_entity(model: TagModel) -> Tag:
    return Tag(
        id=model.id,
        user_id=model.user_id,
        name=model.name,
        category=TagCategory(model.category),
    )


def skill_to_entity(model: SkillModel) -> Skill:
    return Skill(id=model.id, user_id=model.user_id, name=model.name)


def project_to_entity(model: ProjectModel) -> Project:
    return Project(
        id=model.id,
        user_id=model.user_id,
        name=model.name,
        color=model.color,
        archived=model.archived,
    )


def entry_to_entity(model: EntryModel) -> Entry:
    return Entry(
        id=model.id,
        user_id=model.user_id,
        raw_text=model.raw_text,
        entry_date=model.entry_date,
        source=EntrySource(model.source),
        created_at=model.created_at,
        mood=model.mood,
        energy=model.energy,
        project_id=model.project_id,
        tags=[tag_to_entity(t) for t in model.tags],
        skills=[skill_to_entity(s) for s in model.skills],
    )
