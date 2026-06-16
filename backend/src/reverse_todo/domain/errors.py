class DomainError(Exception):
    """Base domain error."""


class EntryNotFoundError(DomainError):
    """Entry does not exist or is not accessible."""


class AccessDeniedError(DomainError):
    """Caller cannot access the resource."""


class UserAlreadyExistsError(DomainError):
    """Email already registered."""


class InvalidCredentialsError(DomainError):
    """Login failed."""


class UserNotFoundError(DomainError):
    """User does not exist."""
