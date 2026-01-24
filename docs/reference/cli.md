# CLI Reference

Complete reference for `dcm` command-line interface.

## Global Options

| Option | Description |
|--------|-------------|
| `-v, --verbose` | Increase verbosity (use `-vv` for debug) |
| `-q, --quiet` | Suppress non-error output |
| `--version` | Show version and exit |
| `--help` | Show help message and exit |

## Commands

### `dcm status`

Show conceptual model coverage status.

```bash
dcm status [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--project-dir PATH` | Path to dbt project root |
| `--silver-paths TEXT` | Override silver layer paths (repeatable) |
| `--gold-paths TEXT` | Override gold layer paths (repeatable) |

---

### `dcm orphans`

List models without `meta.concept` tags.

```bash
dcm orphans [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--project-dir PATH` | Path to dbt project root |
| `--silver-paths TEXT` | Override silver layer paths (repeatable) |
| `--gold-paths TEXT` | Override gold layer paths (repeatable) |

---

### `dcm validate`

Validate conceptual model correspondence. Returns exit code 1 on errors.

```bash
dcm validate [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--project-dir PATH` | Path to dbt project root |
| `--silver-paths TEXT` | Override silver layer paths (repeatable) |
| `--gold-paths TEXT` | Override gold layer paths (repeatable) |
| `--format FORMAT` | Output format: `human` (default), `github`, `markdown` |
| `--no-drafts` | Fail if any concepts/relationships are incomplete |

**Exit codes:**
- `0` — Validation passed
- `1` — Validation errors found

---

### `dcm init`

Initialize dbt-conceptual in a project.

```bash
dcm init [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--project-dir PATH` | Path to dbt project root |

Creates `models/conceptual/conceptual.yml` with starter template.

---

### `dcm sync`

Discover dbt models and sync with conceptual model.

```bash
dcm sync [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--project-dir PATH` | Path to dbt project root |
| `--create-stubs` | Create stub concepts for orphan models |
| `--model TEXT` | Sync only a specific model by name |

---

### `dcm apply`

Apply conceptual model tags to dbt model files.

```bash
dcm apply [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--project-dir PATH` | Path to dbt project root |
| `--propagate-tags` | Write domain/owner tags to model YAML files |
| `--dry-run` | Show what would be changed without modifying files |
| `--models TEXT` | Target specific models (repeatable) |

Useful for propagating conceptual model metadata to dbt models for Unity Catalog tagging.

---

### `dcm export`

Export conceptual model to various formats.

```bash
dcm export --type TYPE --format FORMAT [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--project-dir PATH` | Path to dbt project root |
| `--type TYPE` | What to export (required) |
| `--format FORMAT` | Output format (required) |
| `-o, --output PATH` | Output file (default: stdout) |
| `--no-drafts` | For validation: fail if incomplete |
| `--base REF` | For diff: git ref to compare against |

**Export types and formats:**

| Type | Formats |
|------|---------|
| `diagram` | `svg` |
| `coverage` | `html`, `markdown`, `json` |
| `bus-matrix` | `html`, `markdown`, `json` |
| `status` | `markdown`, `json` |
| `orphans` | `markdown`, `json` |
| `validation` | `markdown`, `json` |
| `diff` | `markdown`, `json` |

See [Export Formats](exports.md) for detailed output documentation.

---

### `dcm serve`

Launch interactive web UI.

```bash
dcm serve [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--project-dir PATH` | Path to dbt project root |
| `--host TEXT` | Host to bind to (default: `127.0.0.1`) |
| `--port INTEGER` | Port to bind to (default: `8050`) |
| `--demo` | Run with demo data (no project required) |

---

### `dcm diff`

Compare conceptual model against a base git reference.

```bash
dcm diff --base REF [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--base REF` | Git ref to compare against (required) |
| `--format FORMAT` | Output: `human` (default), `github`, `json`, `markdown` |
| `--project-dir PATH` | Path to dbt project root |

**Examples:**
```bash
dcm diff --base main
dcm diff --base origin/main --format github
dcm diff --base HEAD~1 --format markdown
```

---

## Exit Codes

| Command | Exit 0 | Exit 1 |
|---------|--------|--------|
| `dcm validate` | No errors | Has errors |
| `dcm validate --no-drafts` | Complete | Has drafts/stubs or errors |
| `dcm diff --format github` | No changes | Has changes |
| Other commands | Success | Error |

## Common Patterns

### CI Validation

```bash
# Basic validation
dcm validate --format github

# Strict validation (no incomplete items)
dcm validate --no-drafts --format github
```

### Coverage Reports

```bash
# Job summary
dcm export --type coverage --format markdown >> $GITHUB_STEP_SUMMARY

# HTML artifact
dcm export --type coverage --format html -o coverage.html
```

### Diff in Pull Requests

```bash
dcm diff --base origin/main --format markdown >> $GITHUB_STEP_SUMMARY
```
