"""Domain entities for backend architecture generation."""

from __future__ import annotations

from dataclasses import dataclass, field

from .value_objects import Description, EndpointDefinition, EntityId, FieldDefinition, Name, Priority


@dataclass(slots=True)
class Requirement:
    """A functional or non-functional backend requirement."""

    name: Name
    description: Description
    priority: Priority = field(default_factory=lambda: Priority("medium"))
    id: EntityId = field(default_factory=EntityId)

    def reprioritize(self, priority: Priority) -> None:
        self.priority = priority


@dataclass(slots=True)
class DatabaseDesign:
    """Database design for a single logical table or collection."""

    name: Name
    description: Description
    fields: tuple[FieldDefinition, ...] = field(default_factory=tuple)
    id: EntityId = field(default_factory=EntityId)

    def add_field(self, field_definition: FieldDefinition) -> None:
        if any(existing.name == field_definition.name for existing in self.fields):
            raise ValueError(f"field already exists: {field_definition.name.value}")
        self.fields = (*self.fields, field_definition)


@dataclass(slots=True)
class APIDesign:
    """HTTP API design for a backend capability."""

    name: Name
    description: Description
    endpoints: tuple[EndpointDefinition, ...] = field(default_factory=tuple)
    id: EntityId = field(default_factory=EntityId)

    def add_endpoint(self, endpoint: EndpointDefinition) -> None:
        if any(
            existing.path == endpoint.path and existing.method == endpoint.method
            for existing in self.endpoints
        ):
            raise ValueError(f"endpoint already exists: {endpoint.method} {endpoint.path}")
        self.endpoints = (*self.endpoints, endpoint)


@dataclass(slots=True)
class Architecture:
    """Aggregate root for a generated backend architecture design."""

    name: Name
    description: Description
    requirements: tuple[Requirement, ...] = field(default_factory=tuple)
    database_designs: tuple[DatabaseDesign, ...] = field(default_factory=tuple)
    api_designs: tuple[APIDesign, ...] = field(default_factory=tuple)
    id: EntityId = field(default_factory=EntityId)

    def add_requirement(self, requirement: Requirement) -> None:
        if any(existing.name == requirement.name for existing in self.requirements):
            raise ValueError(f"requirement already exists: {requirement.name.value}")
        self.requirements = (*self.requirements, requirement)

    def add_database_design(self, database_design: DatabaseDesign) -> None:
        if any(existing.name == database_design.name for existing in self.database_designs):
            raise ValueError(f"database design already exists: {database_design.name.value}")
        self.database_designs = (*self.database_designs, database_design)

    def add_api_design(self, api_design: APIDesign) -> None:
        if any(existing.name == api_design.name for existing in self.api_designs):
            raise ValueError(f"API design already exists: {api_design.name.value}")
        self.api_designs = (*self.api_designs, api_design)
