"""Tests for validation logic."""

from pathlib import Path

from dbt_conceptual.config import Config
from dbt_conceptual.state import ConceptState, ProjectState, RelationshipState
from dbt_conceptual.validator import Severity, Validator


def test_validate_concept_required_fields() -> None:
    """Test validation of concept required fields."""
    config = Config(project_dir=Path("/tmp"))
    state = ProjectState()

    # Add a complete concept missing fields
    state.concepts["customer"] = ConceptState(
        name="Customer",
        domain=None,  # Missing
        owner=None,  # Missing
        definition=None,  # Missing
        status="complete",
    )

    validator = Validator(config, state)
    issues = validator.validate()

    # Should have an error for missing fields
    errors = [i for i in issues if i.severity == Severity.ERROR]
    assert len(errors) > 0
    assert any("missing required fields" in i.message for i in errors)


def test_validate_relationship_endpoints() -> None:
    """Test validation of relationship endpoints."""
    config = Config(project_dir=Path("/tmp"))
    state = ProjectState()

    # Add a relationship with non-existent concepts
    state.relationships["customer:places:order"] = RelationshipState(
        name="places",
        from_concept="customer",
        to_concept="order",
    )

    validator = Validator(config, state)
    issues = validator.validate()

    # Should have errors for missing concepts
    errors = [i for i in issues if i.severity == Severity.ERROR]
    assert len(errors) >= 2  # One for each missing concept


def test_validate_deprecated_references() -> None:
    """Test validation warns about deprecated concept usage."""
    config = Config(project_dir=Path("/tmp"))
    state = ProjectState()

    # Add a deprecated concept that's still being used
    state.concepts["old_customer"] = ConceptState(
        name="Old Customer",
        domain="party",
        owner="data_team",
        definition="Deprecated",
        status="deprecated",
        gold_models=["dim_old_customer"],
    )

    validator = Validator(config, state)
    issues = validator.validate()

    # Should have a warning
    warnings = [i for i in issues if i.severity == Severity.WARNING]
    assert len(warnings) > 0
    assert any("deprecated" in i.message.lower() for i in warnings)


def test_validate_gold_only_warning() -> None:
    """Test that gold-only concepts generate warnings."""
    config = Config(project_dir=Path("/tmp"))
    state = ProjectState()

    # Add a concept with only gold models
    state.concepts["derived"] = ConceptState(
        name="Derived Metric",
        domain="analytics",
        owner="data_team",
        definition="A derived metric",
        status="complete",
        gold_models=["fact_derived"],
        silver_models=[],
    )

    validator = Validator(config, state)
    issues = validator.validate()

    # Should have a warning about gold-only
    warnings = [i for i in issues if i.severity == Severity.WARNING]
    assert any("gold models but no silver" in i.message for i in warnings)


def test_validator_summary() -> None:
    """Test validator summary counts."""
    config = Config(project_dir=Path("/tmp"))
    state = ProjectState()

    # Add various issues
    state.concepts["stub"] = ConceptState(name="Stub", status="stub")
    state.concepts["incomplete"] = ConceptState(
        name="Incomplete", status="complete"
    )  # Missing required fields

    validator = Validator(config, state)
    validator.validate()

    summary = validator.get_summary()
    assert "errors" in summary
    assert "warnings" in summary
    assert "info" in summary
