# Guides

Practical guides for working with dbt-conceptual in your projects.

## Adoption Workflows

New to dbt-conceptual? Start here:

- **[Choosing Your Approach](adoption/choosing-your-approach.md)** — Find the right path for your situation
- **[Top-Down: Conceptual First](adoption/greenfield-top-down.md)** — For new projects with clear requirements
- **[Bottom-Up: Models First](adoption/greenfield-bottom-up.md)** — For fast iteration, formalize later
- **[Brownfield Adoption](adoption/brownfield-adoption.md)** — For existing projects with governance pressure
- **[Working with Governance](adoption/working-with-governance.md)** — The collaboration handshake

---

## Getting Things Done

- **[Defining Concepts](defining-concepts.md)** — Best practices for writing concept definitions
- **[Tagging dbt Models](tagging-models.md)** — How to link models to concepts
- **[Validation & Messages](validation.md)** — Understanding and resolving validation issues
- **[CI/CD Integration](ci-integration.md)** — Adding dbt-conceptual to your pipeline

## Common Workflows

### Starting Fresh

1. Run `dcm init` to create the conceptual model
2. Define your domains and key concepts
3. Add `meta.concept` tags to existing models
4. Run `dcm validate` to check for issues

### Adopting in an Existing Project

1. Run `dcm sync --create-stubs` to generate concept placeholders
2. Review and enrich the generated stubs with definitions
3. Assign domains and owners
4. Run `dcm status` to track progress

### Day-to-Day Development

1. Add new concepts when requirements emerge
2. Tag new models as they're created
3. Run validation in CI to catch drift
4. Review conceptual changes in PRs
