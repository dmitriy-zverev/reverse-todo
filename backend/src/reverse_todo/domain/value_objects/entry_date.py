from dataclasses import dataclass
from datetime import date, datetime
from zoneinfo import ZoneInfo


@dataclass(frozen=True, slots=True)
class EntryDate:
    """Calendar day of the action in the user's timezone."""

    value: date

    @classmethod
    def today_in_timezone(cls, tz_name: str) -> "EntryDate":
        tz = ZoneInfo(tz_name)
        return cls(datetime.now(tz).date())

    @classmethod
    def from_optional(cls, value: date | None, tz_name: str) -> "EntryDate":
        if value is not None:
            return cls(value)
        return cls.today_in_timezone(tz_name)
