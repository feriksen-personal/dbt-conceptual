# Top-Down: Conceptual First

**"We know what we're building."**

Start with the conceptual model, then implement. Governance alignment from day one.

![Top-down workflow](../../assets/workflow-greenfield-top-down.svg)

---

## When to Use This Approach

- Regulated industries (finance, healthcare, insurance)
- Clear domain model from business stakeholders
- Governance office engaged early in the project
- Compliance requirements known upfront (GDPR, SOX, HIPAA)
- You want to avoid rework later

---

## The Workflow

### Step 1: Define Taxonomy (Optional)

If your organization has established vocabulary — codify it first:

```yaml
# models/conceptual/taxonomy.yml
version: 1

confidentiality:
  - key: public
    name: "Public"
    brief: "No restrictions"
  - key: internal
    name: "Internal"
    brief: "Employees only"
  - key: confidential
    name: "Confidential"
    brief: "Need-to-know basis"

retention:
  - key: short
    brief: "90 days"
  - key: standard
    brief: "3 years"
  - key: extended
    brief: "7 years"

regulatory:
  - key: GDPR
    brief: "EU data protection"
  - key: SOX
    brief: "Financial controls"
```

**Why do this first?**
- Prevents domain arguments later
- Governance office can validate the vocabulary
- Values are validated — typos caught in CI

**No taxonomy file?** That's fine. Free text is allowed. Add one when you're ready.

---

### Step 2: Define Concepts

#### Using the UI

1. Open dbt-conceptual
2. Navigate to **Canvas**
3. Click **Add Concept**
4. Fill in properties: Name, Domain, Owner, Description
5. Draw relationships between concepts
6. Click **Save** — YAML is generated automatically

#### Using YAML

```yaml
# models/conceptual/conceptual.yml
concepts:
  customer:
    name: "Customer"
    domain: party
    owner: commercial-analytics
    maturity: high
    confidentiality: confidential  # validated against taxonomy
    regulatory: [GDPR]
    description: |
      A party who has purchased or may purchase products/services.
      The primary entity for commercial reporting.

  order:
    name: "Order"
    domain: transaction
    owner: commercial-analytics
    maturity: high
    description: |
      A confirmed request to purchase products/services.

relationships:
  - name: places
    from: customer
    to: order
    cardinality: "1:N"
    description: "A customer places zero or more orders"
```

---

### Step 3: Share for Review

Your conceptual model lives in Git. Share it with your governance office:

**Option A: Link to the file**
```
https://github.com/your-org/your-repo/blob/main/models/conceptual/conceptual.yml
```

**Option B: Export for review**
```bash
dcm export --format html --output conceptual-model.html
dcm export --format pdf --output conceptual-model.pdf
```

**Option C: Share the UI**

Give governance office access to the web UI — they can review visually without touching YAML.

The review is async. No meetings required. They comment on the PR or send feedback.

---

### Step 4: Build dbt Models

With concepts defined and approved, build your models and tag them:

```yaml
# models/marts/dim_customer.yml
models:
  - name: dim_customer
    description: "Customer dimension"
    meta:
      concept: customer
    columns:
      - name: customer_id
        description: "Primary key"
```

The `meta.concept` tag links the physical model to the conceptual entity.

---

### Step 5: Validate in CI

Add validation to your CI pipeline:

```yaml
# .github/workflows/ci.yml
- name: Validate conceptual model
  run: dcm validate

- name: Check coverage
  run: dcm coverage --min 80
```

![CI governance validation](../../assets/workflow-ci-governance.svg)

**What gets validated:**
- All gold models have concept tags
- Taxonomy values are valid
- Required fields are present (if configured)
- No deprecated concepts in use

---

## Configuration Options

Start permissive, tighten over time:

```yaml
# dbt_project.yml
vars:
  dbt_conceptual:
    governance:
      # Start with these (permissive)
      require_domain: true
      require_owner: true
      
      # Add these later (stricter)
      require_maturity: false
      require_confidentiality: false
      enforce_taxonomy_validation: false
```

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Trying to model everything at once | Start with gold layer only |
| Skipping governance review | They'll reject it later — engage early |
| Making CI fail immediately | Start with warnings, enable errors when ready |
| Over-engineering taxonomy | Start simple, add complexity as needed |

---

## Outcome

✓ Governance aligned from day one  
✓ Shared vocabulary lives in code  
✓ No rework when audit comes  
✓ CI enforces standards automatically  
✓ Tags propagate to Unity Catalog  

---

## Next Steps

- [Working with Governance](working-with-governance.md) — The collaboration handshake
- [CI/CD Integration](../ci-integration.md) — Detailed pipeline setup
- [Validation & Messages](../validation.md) — Understanding validation output
