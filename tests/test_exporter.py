"""Tests for export functionality."""

from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml
from click.testing import CliRunner

from dbt_conceptual.cli import export
from dbt_conceptual.config import Config
from dbt_conceptual.exporter import export_mermaid
from dbt_conceptual.parser import StateBuilder


def test_export_mermaid_basic() -> None:
    """Test basic Mermaid export with concepts and relationships."""
    with TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create dbt_project.yml
        with open(tmppath / "dbt_project.yml", "w") as f:
            yaml.dump({"name": "test"}, f)

        # Create conceptual.yml
        conceptual_dir = tmppath / "models" / "conceptual"
        conceptual_dir.mkdir(parents=True)

        conceptual_data = {
            "version": 1,
            "concepts": {
                "customer": {
                    "name": "Customer",
                    "owner": "data_team",
                    "definition": "A person who buys products",
                    "status": "complete",
                },
                "order": {
                    "name": "Order",
                    "status": "complete",
                },
            },
            "relationships": [
                {
                    "name": "places",
                    "from": "customer",
                    "to": "order",
                    "cardinality": "1:N",
                }
            ],
        }

        with open(conceptual_dir / "conceptual.yml", "w") as f:
            yaml.dump(conceptual_data, f)

        config = Config.load(project_dir=tmppath)
        builder = StateBuilder(config)
        state = builder.build()

        # Export to string
        output = StringIO()
        export_mermaid(state, output)
        result = output.getvalue()

        # Verify output
        assert "erDiagram" in result
        assert "CUSTOMER" in result
        assert "ORDER" in result
        assert "places" in result
        assert "Owner: data_team" in result
        assert "Definition: A person who buys products" in result


def test_export_mermaid_with_domains() -> None:
    """Test Mermaid export with domains."""
    with TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create dbt_project.yml
        with open(tmppath / "dbt_project.yml", "w") as f:
            yaml.dump({"name": "test"}, f)

        # Create conceptual.yml with domains
        conceptual_dir = tmppath / "models" / "conceptual"
        conceptual_dir.mkdir(parents=True)

        conceptual_data = {
            "version": 1,
            "domains": {"party": {"name": "Party", "color": "#E3F2FD"}},
            "concepts": {"customer": {"name": "Customer", "domain": "party"}},
        }

        with open(conceptual_dir / "conceptual.yml", "w") as f:
            yaml.dump(conceptual_data, f)

        config = Config.load(project_dir=tmppath)
        builder = StateBuilder(config)
        state = builder.build()

        output = StringIO()
        export_mermaid(state, output)
        result = output.getvalue()

        assert "CUSTOMER" in result


def test_export_mermaid_with_implementations() -> None:
    """Test Mermaid export shows which models implement concepts."""
    with TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create dbt_project.yml
        with open(tmppath / "dbt_project.yml", "w") as f:
            yaml.dump({"name": "test"}, f)

        # Create conceptual.yml
        conceptual_dir = tmppath / "models" / "conceptual"
        conceptual_dir.mkdir(parents=True)

        conceptual_data = {
            "version": 1,
            "concepts": {"customer": {"name": "Customer"}},
            "relationships": [{"name": "places", "from": "customer", "to": "order"}],
        }

        with open(conceptual_dir / "conceptual.yml", "w") as f:
            yaml.dump(conceptual_data, f)

        # Create models
        gold_dir = tmppath / "models" / "gold"
        gold_dir.mkdir(parents=True)

        with open(gold_dir / "schema.yml", "w") as f:
            yaml.dump(
                {
                    "version": 2,
                    "models": [
                        {"name": "dim_customer", "meta": {"concept": "customer"}},
                        {
                            "name": "fact_orders",
                            "meta": {"realizes": ["customer:places:order"]},
                        },
                    ],
                },
                f,
            )

        config = Config.load(project_dir=tmppath)
        builder = StateBuilder(config)
        state = builder.build()

        output = StringIO()
        export_mermaid(state, output)
        result = output.getvalue()

        assert "Gold: dim_customer" in result
        assert "Realized by: fact_orders" in result


def test_cli_export_mermaid_to_stdout() -> None:
    """Test export command outputs to stdout."""
    runner = CliRunner()

    with TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create dbt_project.yml
        with open(tmppath / "dbt_project.yml", "w") as f:
            yaml.dump({"name": "test"}, f)

        # Create conceptual.yml
        conceptual_dir = tmppath / "models" / "conceptual"
        conceptual_dir.mkdir(parents=True)

        conceptual_data = {
            "version": 1,
            "concepts": {"customer": {"name": "Customer"}},
        }

        with open(conceptual_dir / "conceptual.yml", "w") as f:
            yaml.dump(conceptual_data, f)

        # Run export command
        result = runner.invoke(
            export, ["--project-dir", str(tmppath), "--format", "mermaid"]
        )

        assert result.exit_code == 0
        assert "erDiagram" in result.output
        assert "CUSTOMER" in result.output


def test_cli_export_mermaid_to_file() -> None:
    """Test export command writes to file."""
    runner = CliRunner()

    with TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create dbt_project.yml
        with open(tmppath / "dbt_project.yml", "w") as f:
            yaml.dump({"name": "test"}, f)

        # Create conceptual.yml
        conceptual_dir = tmppath / "models" / "conceptual"
        conceptual_dir.mkdir(parents=True)

        conceptual_data = {
            "version": 1,
            "concepts": {"customer": {"name": "Customer"}},
        }

        with open(conceptual_dir / "conceptual.yml", "w") as f:
            yaml.dump(conceptual_data, f)

        # Run export command with output file
        output_file = tmppath / "diagram.mmd"
        result = runner.invoke(
            export,
            [
                "--project-dir",
                str(tmppath),
                "--format",
                "mermaid",
                "-o",
                str(output_file),
            ],
        )

        assert result.exit_code == 0
        assert "Exported to" in result.output
        assert output_file.exists()

        # Check file content
        with open(output_file) as f:
            content = f.read()
            assert "erDiagram" in content
            assert "CUSTOMER" in content


def test_cli_export_without_conceptual_file() -> None:
    """Test export command fails gracefully without conceptual.yml."""
    runner = CliRunner()

    with TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create only dbt_project.yml
        with open(tmppath / "dbt_project.yml", "w") as f:
            yaml.dump({"name": "test"}, f)

        result = runner.invoke(export, ["--project-dir", str(tmppath)])

        assert result.exit_code != 0
        assert "conceptual.yml not found" in result.output
