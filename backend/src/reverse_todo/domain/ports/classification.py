from typing import Protocol

from reverse_todo.domain.entities import ClassificationSuggestion, Project, Skill, Tag
from reverse_todo.domain.value_objects.category import TagCategory


class UserContext(Protocol):
  @property
  def user_id(self): ...

  @property
  def timezone(self) -> str: ...

  @property
  def projects(self) -> list[Project]: ...

  @property
  def tags(self) -> list[Tag]: ...

  @property
  def skills(self) -> list[Skill]: ...


class ClassificationProvider(Protocol):
    async def classify(self, text: str, context: UserContext) -> ClassificationSuggestion: ...
