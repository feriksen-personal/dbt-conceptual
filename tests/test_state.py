"""Tests for state models."""

from dbt_conceptual.state import ConceptState, ProjectState, RelationshipState


def test_concept_state_creation() -> None:
    """Test creating a ConceptState."""
    concept = ConceptState(
        name="Customer",
        domain="party",
        owner="data_team",
        definition="A person who buys products",
        status="complete",
    )

    assert concept.name == "Customer"
    assert concept.domain == "party"
    assert concept.owner == "data_team"
    assert concept.definition == "A person who buys products"
    assert concept.status == "complete"
    assert concept.silver_models == []
    assert concept.gold_models == []


def test_relationship_state_creation() -> None:
    """Test creating a RelationshipState."""
    rel = RelationshipState(
        name="places",
        from_concept="customer",
        to_concept="order",
        cardinality="1:N",
    )

    assert rel.name == "places"
    assert rel.from_concept == "customer"
    assert rel.to_concept == "order"
    assert rel.cardinality == "1:N"
    assert rel.realized_by == []


def test_project_state_creation() -> None:
    """Test creating a ProjectState."""
    state = ProjectState()

    assert state.concepts == {}
    assert state.relationships == {}
    assert state.groups == {}
    assert state.domains == {}
    assert state.orphan_models == []
    assert state.metadata == {}
