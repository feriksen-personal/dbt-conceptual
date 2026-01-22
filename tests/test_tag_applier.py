"""Tests for tag applier."""

from pathlib import Path
from unittest.mock import patch

from dbt_conceptual.config import Config, TagValidationConfig, ValidationConfig
from dbt_conceptual.state import (
    ConceptState,
    DomainState,
    ModelInfo,
    ProjectState,
)
from dbt_conceptual.tag_applier import TagApplier


def test_compute_changes_no_changes_needed() -> None:
    """Test that no changes are computed when tags are correct."""
    validation_config = ValidationConfig(
        tag_validation=TagValidationConfig(enabled=True)
    )
    config = Config(project_dir=Path("/tmp"), validation=validation_config)
    state = ProjectState()

    # Add concept and model with correct tags
    state.concepts["customer"] = ConceptState(
        name="Customer",
        domain="party",
        owner="data_team",
        silver_models=["stg_customer"],
    )
    state.domains["party"] = DomainState(name="party", display_name="Party")
    state.models["stg_customer"] = ModelInfo(
        name="stg_customer",
        concept="customer",
        domain_tags=["party"],
        owner_tag="data_team",
        layer="silver",
    )

    applier = TagApplier(config, state)

    # Mock _find_model_file to return a fake path
    with patch.object(
        applier, "_find_model_file", return_value=Path("/tmp/schema.yml")
    ):
        changes = applier.compute_changes()

    # Should have no changes
    assert len(changes) == 0


def test_compute_changes_missing_domain() -> None:
    """Test that missing domain tag generates a change."""
    validation_config = ValidationConfig(
        tag_validation=TagValidationConfig(enabled=True)
    )
    config = Config(project_dir=Path("/tmp"), validation=validation_config)
    state = ProjectState()

    # Add concept and model without domain tag
    state.concepts["customer"] = ConceptState(
        name="Customer",
        domain="party",
        owner="data_team",
        silver_models=["stg_customer"],
    )
    state.domains["party"] = DomainState(name="party", display_name="Party")
    state.models["stg_customer"] = ModelInfo(
        name="stg_customer",
        concept="customer",
        domain_tags=[],  # Missing
        owner_tag="data_team",
        layer="silver",
    )

    applier = TagApplier(config, state)

    # Mock _find_model_file to return a fake path
    with patch.object(
        applier, "_find_model_file", return_value=Path("/tmp/schema.yml")
    ):
        changes = applier.compute_changes()

    # Should have one change for missing domain
    assert len(changes) == 1
    assert changes[0].model_name == "stg_customer"
    assert "party" in changes[0].domain_tags_to_add


def test_compute_changes_wrong_owner() -> None:
    """Test that wrong owner tag generates a change."""
    validation_config = ValidationConfig(
        tag_validation=TagValidationConfig(enabled=True)
    )
    config = Config(project_dir=Path("/tmp"), validation=validation_config)
    state = ProjectState()

    # Add concept and model with wrong owner
    state.concepts["customer"] = ConceptState(
        name="Customer",
        domain="party",
        owner="data_team",
        silver_models=["stg_customer"],
    )
    state.domains["party"] = DomainState(name="party", display_name="Party")
    state.models["stg_customer"] = ModelInfo(
        name="stg_customer",
        concept="customer",
        domain_tags=["party"],
        owner_tag="wrong_team",
        layer="silver",
    )

    applier = TagApplier(config, state)

    # Mock _find_model_file to return a fake path
    with patch.object(
        applier, "_find_model_file", return_value=Path("/tmp/schema.yml")
    ):
        changes = applier.compute_changes()

    # Should have one change for wrong owner
    assert len(changes) == 1
    assert changes[0].owner_tag_to_add == "data_team"
    assert changes[0].owner_tag_to_remove == "wrong_team"


def test_compute_changes_scoped_to_models() -> None:
    """Test that changes can be scoped to specific models."""
    validation_config = ValidationConfig(
        tag_validation=TagValidationConfig(enabled=True)
    )
    config = Config(project_dir=Path("/tmp"), validation=validation_config)
    state = ProjectState()

    # Add two models with missing tags
    state.concepts["customer"] = ConceptState(
        name="Customer",
        domain="party",
        silver_models=["stg_customer", "stg_customer_v2"],
    )
    state.domains["party"] = DomainState(name="party", display_name="Party")
    state.models["stg_customer"] = ModelInfo(
        name="stg_customer",
        concept="customer",
        domain_tags=[],
        layer="silver",
    )
    state.models["stg_customer_v2"] = ModelInfo(
        name="stg_customer_v2",
        concept="customer",
        domain_tags=[],
        layer="silver",
    )

    applier = TagApplier(config, state)

    # Mock _find_model_file to return a fake path
    with patch.object(
        applier, "_find_model_file", return_value=Path("/tmp/schema.yml")
    ):
        # Scope to only stg_customer
        changes = applier.compute_changes(model_names=["stg_customer"])

    # Should have one change
    assert len(changes) == 1
    assert changes[0].model_name == "stg_customer"
