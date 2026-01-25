# CLI Reference

This is the complete reference for the `dbt-conceptual` command-line interface.

---

## Global Options

```bash
dbt-conceptual [OPTIONS] COMMAND
```

| Option | Description |
|--------|-------------|
| `-v, --verbose` | Show more detail (use `-vv` for debug output) |
| `-q, --quiet` | Show only errors |
| `--version` | Show version and exit |
| `--help` | Show help and exit |

You can also use `dcm` as a shorthand:

```bash
dcm status
dcm validate
dcm serve
```

---

## Commands

### init

Creates a starter `conceptual.yml` in your project.

```bash
dcm init [--project-dir PATH]
```

This gives you a template to start from:

```yaml
version: 1

domains: {}

concepts: {}

relationships: []
```

---

### status

Shows coverage — how many concepts have implementing models.

```bash
dcm status [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--project-dir PATH` | Path to dbt project |
| `--silver-paths TEXT` | Override silver layer paths (can repeat) |
| `--gold-paths TEXT` | Override gold layer paths (can repeat) |

Example output:

```
Coverage Summary
────────────────────────────────────
Gold layer:    8/10 models   (80%)
Silver layer:  5/15 models   (33%)

Concepts: 12 total
  - 8 complete
  - 3 draft
  - 1 stub

Domains:
  party: 3/3 complete
  transaction: 4/5 complete (1 draft)
```

---

### validate

Checks for issues in your conceptual model. Useful in CI.

```bash
dcm validate [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--project-dir PATH` | Path to dbt project |
| `--format FORMAT` | Output format: `human`, `github`, or `markdown` |
| `--no-drafts` | Fail if any concepts are incomplete |

Exit codes:
- `0` — Everything looks good
- `1` — There are validation errors

The `--no-drafts` flag is useful when you want to ensure everything is fully documented before merging.

---

### sync

Discovers dbt models and updates the conceptual model.

```bash
dcm sync [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--project-dir PATH` | Path to dbt project |
| `--create-stubs` | Create placeholder concepts for untagged models |
| `--model TEXT` | Sync only a specific model |

The `--create-stubs` option is helpful when adopting dbt-conceptual in an existing project — it gives you a starting point to enrich.

---

### orphans

Lists models that don't have `meta.concept` tags.

```bash
dcm orphans [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--project-dir PATH` | Path to dbt project |
| `--silver-paths TEXT` | Override silver layer paths |
| `--gold-paths TEXT` | Override gold layer paths |

---

### apply

Writes metadata from your conceptual model back to dbt model files.

```bash
dcm apply [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--project-dir PATH` | Path to dbt project |
| `--propagate-tags` | Write domain/owner tags to model YAML |
| `--dry-run` | Show what would change without writing |
| `--models TEXT` | Only apply to specific models |

This is useful if you want domain and owner information to flow from your conceptual model into your dbt models — for example, to feed Unity Catalog tags.

---

### export

Exports reports in various formats.

```bash
dcm export --type TYPE --format FORMAT [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--type TYPE` | What to export (required) |
| `--format FORMAT` | Output format (required) |
| `-o, --output PATH` | Write to file instead of stdout |
| `--no-drafts` | For validation: fail if incomplete |
| `--base REF` | For diff: git ref to compare against |

**What you can export:**

| Type | Available Formats |
|------|-------------------|
| `diagram` | svg |
| `coverage` | html, markdown, json |
| `bus-matrix` | html, markdown, json |
| `status` | markdown, json |
| `orphans` | markdown, json |
| `validation` | markdown, json |
| `diff` | markdown, json |

Examples:

```bash
# Coverage as markdown (nice for CI job summaries)
dcm export --type coverage --format markdown

# Bus matrix as HTML
dcm export --type bus-matrix --format html -o matrix.html

# SVG diagram
dcm export --type diagram --format svg -o model.svg
```

---

### diff

Compares your conceptual model against a git reference.

```bash
dcm diff --base REF [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--base REF` | Git ref to compare against (required) |
| `--format FORMAT` | Output: `human`, `github`, `json`, or `markdown` |
| `--project-dir PATH` | Path to dbt project |

Examples:

```bash
# Compare against main branch
dcm diff --base main

# Markdown output for PR summaries
dcm diff --base origin/main --format markdown

# JSON for automation
dcm diff --base HEAD~1 --format json
```

---

### serve

Launches the web UI.

```bash
dcm serve [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--project-dir PATH` | Path to dbt project |
| `--host TEXT` | Host to bind to (default: `127.0.0.1`) |
| `--port INT` | Port to bind to (default: `8050`) |
| `--demo` | Launch with sample data (no project needed) |

The `--demo` flag is useful if you want to explore the UI without setting up a project first.

```bash
# Try it out
dcm serve --demo

# Normal usage
dcm serve

# Custom port
dcm serve --port 3000
```

---

## Exit Codes

| Command | Exit 0 | Exit 1 |
|---------|--------|--------|
| `validate` | No errors | Has errors |
| `validate --no-drafts` | All complete | Has drafts/stubs |
| `diff` | Always succeeds | — |
| Other commands | Success | Error |

---

## Common Patterns

**CI validation:**
```bash
dcm validate --format markdown >> $GITHUB_STEP_SUMMARY
```

**Coverage in job summary:**
```bash
dcm export --type coverage --format markdown >> $GITHUB_STEP_SUMMARY
```

**PR diff:**
```bash
dcm diff --base origin/main --format markdown >> $GITHUB_STEP_SUMMARY
```

**Check for changes in automation:**
```bash
dcm diff --base main --format json | jq '.has_changes'
```
