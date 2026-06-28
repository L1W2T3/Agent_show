import pytest

from backend_architect_agent.domain.architecture import (
    APIDesign,
    Architecture,
    DatabaseDesign,
    Description,
    EndpointDefinition,
    FieldDefinition,
    Name,
    Priority,
    Requirement,
)


def test_requirement_requires_valid_value_objects_and_can_be_reprioritized() -> None:
    requirement = Requirement(
        name=Name("User ordering"),
        description=Description("Customers can place food orders."),
    )

    requirement.reprioritize(Priority("critical"))

    assert requirement.name.value == "User ordering"
    assert requirement.priority.value == "critical"


def test_empty_name_is_invalid() -> None:
    with pytest.raises(ValueError, match="name must not be empty"):
        Name("   ")


def test_database_design_adds_unique_fields() -> None:
    design = DatabaseDesign(
        name=Name("orders"),
        description=Description("Stores customer orders."),
    )
    field = FieldDefinition(name=Name("id"), data_type=Name("uuid"))

    design.add_field(field)

    assert design.fields == (field,)
    with pytest.raises(ValueError, match="field already exists"):
        design.add_field(field)


def test_api_design_adds_unique_endpoints_and_normalizes_method() -> None:
    api = APIDesign(
        name=Name("Orders API"),
        description=Description("Manages customer orders."),
    )
    endpoint = EndpointDefinition(
        path="/orders",
        method="post",
        description=Description("Create an order."),
    )

    api.add_endpoint(endpoint)

    assert api.endpoints[0].method == "POST"
    with pytest.raises(ValueError, match="endpoint already exists"):
        api.add_endpoint(endpoint)


def test_endpoint_path_must_be_absolute() -> None:
    with pytest.raises(ValueError, match="path must start"):
        EndpointDefinition(
            path="orders",
            method="GET",
            description=Description("List orders."),
        )


def test_architecture_aggregates_unique_domain_components() -> None:
    architecture = Architecture(
        name=Name("Food Delivery Platform"),
        description=Description("Backend architecture for food delivery."),
    )
    requirement = Requirement(
        name=Name("Ordering"),
        description=Description("Customers can place orders."),
    )
    database_design = DatabaseDesign(
        name=Name("orders"),
        description=Description("Order persistence model."),
    )
    api_design = APIDesign(
        name=Name("Orders API"),
        description=Description("Order HTTP API."),
    )

    architecture.add_requirement(requirement)
    architecture.add_database_design(database_design)
    architecture.add_api_design(api_design)

    assert architecture.requirements == (requirement,)
    assert architecture.database_designs == (database_design,)
    assert architecture.api_designs == (api_design,)

    with pytest.raises(ValueError, match="requirement already exists"):
        architecture.add_requirement(requirement)
