"""Value objects for backend architecture design concepts."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping
from uuid import UUID, uuid4


def _ensure_non_empty(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


@dataclass(frozen=True, slots=True)
class EntityId:
    """Stable identity value object for domain entities."""

    value: UUID = field(default_factory=uuid4)


@dataclass(frozen=True, slots=True)
class Name:
    """Human-readable, non-empty name."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _ensure_non_empty(self.value, "name"))


@dataclass(frozen=True, slots=True)
class Description:
    """Human-readable, non-empty description."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _ensure_non_empty(self.value, "description"))


@dataclass(frozen=True, slots=True)
class Priority:
    """Requirement priority with constrained values."""

    value: str

    _allowed = frozenset({"low", "medium", "high", "critical"})

    def __post_init__(self) -> None:
        normalized = _ensure_non_empty(self.value, "priority").lower()
        if normalized not in self._allowed:
            allowed = ", ".join(sorted(self._allowed))
            raise ValueError(f"priority must be one of: {allowed}")
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True, slots=True)
class FieldDefinition:
    """Definition of a database field/column."""

    name: Name
    data_type: Name
    nullable: bool = False
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True, slots=True)
class EndpointDefinition:
    """Definition of an API endpoint."""

    path: str
    method: str
    description: Description

    _allowed_methods = frozenset({"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"})

    def __post_init__(self) -> None:
        normalized_path = _ensure_non_empty(self.path, "path")
        if not normalized_path.startswith("/"):
            raise ValueError("path must start with '/'")
        normalized_method = _ensure_non_empty(self.method, "method").upper()
        if normalized_method not in self._allowed_methods:
            allowed = ", ".join(sorted(self._allowed_methods))
            raise ValueError(f"method must be one of: {allowed}")
        object.__setattr__(self, "path", normalized_path)
        object.__setattr__(self, "method", normalized_method)
