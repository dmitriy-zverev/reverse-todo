from datetime import date, datetime
from uuid import UUID, uuid4

from reverse_todo.domain.entities import Entry, Project, Skill, Tag, User
from reverse_todo.domain.value_objects.category import TagCategory


class FakeUserRepository:
    def __init__(self) -> None:
        self.users: dict[UUID, User] = {}
        self.by_email: dict[str, UUID] = {}

    async def get_by_id(self, user_id: UUID) -> User | None:
        return self.users.get(user_id)

    async def get_by_email(self, email: str) -> User | None:
        uid = self.by_email.get(email)
        return self.users.get(uid) if uid else None

    async def create(self, user: User) -> User:
        self.users[user.id] = user
        self.by_email[user.email] = user.id
        return user

    async def update_timezone(self, user_id: UUID, timezone: str) -> User:
        user = self.users[user_id]
        user.timezone = timezone
        return user


class FakeTagRepository:
    def __init__(self) -> None:
        self.tags: dict[UUID, Tag] = {}

    async def list_by_user(self, user_id: UUID) -> list[Tag]:
        return [t for t in self.tags.values() if t.user_id == user_id]

    async def get_or_create(self, user_id: UUID, name: str, category: TagCategory) -> Tag:
        for tag in self.tags.values():
            if tag.user_id == user_id and tag.name == name:
                return tag
        tag = Tag(id=uuid4(), user_id=user_id, name=name, category=category)
        self.tags[tag.id] = tag
        return tag


class FakeProjectRepository:
    def __init__(self) -> None:
        self.projects: dict[UUID, Project] = {}

    async def list_by_user(self, user_id: UUID) -> list[Project]:
        return [p for p in self.projects.values() if p.user_id == user_id and not p.archived]

    async def get_or_create(self, user_id: UUID, name: str, color: str) -> Project:
        for p in self.projects.values():
            if p.user_id == user_id and p.name == name:
                return p
        project = Project(id=uuid4(), user_id=user_id, name=name, color=color)
        self.projects[project.id] = project
        return project

    async def create(self, project: Project) -> Project:
        self.projects[project.id] = project
        return project


class FakeSkillRepository:
    def __init__(self) -> None:
        self.skills: dict[UUID, Skill] = {}

    async def list_by_user(self, user_id: UUID) -> list[Skill]:
        return [s for s in self.skills.values() if s.user_id == user_id]

    async def get_or_create(self, user_id: UUID, name: str) -> Skill:
        for s in self.skills.values():
            if s.user_id == user_id and s.name == name:
                return s
        skill = Skill(id=uuid4(), user_id=user_id, name=name)
        self.skills[skill.id] = skill
        return skill


class FakeEntryRepository:
    def __init__(self) -> None:
        self.entries: dict[UUID, Entry] = {}

    async def create(self, entry: Entry) -> Entry:
        self.entries[entry.id] = entry
        return entry

    async def get_by_id(self, user_id: UUID, entry_id: UUID) -> Entry | None:
        entry = self.entries.get(entry_id)
        if entry is None or entry.user_id != user_id:
            return None
        return entry

    async def list_by_date_range(
        self, user_id: UUID, date_from: date, date_to: date
    ) -> list[Entry]:
        return [
            e
            for e in self.entries.values()
            if e.user_id == user_id and date_from <= e.entry_date <= date_to
        ]

    async def list_by_user(self, user_id: UUID) -> list[Entry]:
        return [e for e in self.entries.values() if e.user_id == user_id]

    async def update(self, entry: Entry) -> Entry:
        self.entries[entry.id] = entry
        return entry

    async def delete(self, user_id: UUID, entry_id: UUID) -> bool:
        entry = await self.get_by_id(user_id, entry_id)
        if entry is None:
            return False
        del self.entries[entry_id]
        return True


class FakeStore:
    def __init__(self) -> None:
        self.users = FakeUserRepository()
        self.entries = FakeEntryRepository()
        self.tags = FakeTagRepository()
        self.projects = FakeProjectRepository()
        self.skills = FakeSkillRepository()
