# Bottom-Up: Models First

**"We're iterating fast. We'll formalize later."**

Build your models, add concept tags as you go, then generate stubs and enrich them.

---

## When to Use This Approach

- Startup or fast-moving team
- Requirements still evolving
- Need to ship first, document later
- Exploratory data work
- Governance can wait (but not forever)

---

## The Workflow

### Step 1: Build Models as Normal

Just build your dbt models. Nothing special yet.

```sql
-- models/marts/dim_customer.sql
SELECT
    customer_id,
    customer_name,
    email,
    created_at
FROM {{ ref('stg_customers') }}
```

---

### Step 2: Add Concept Tags

As you build, add lightweight `meta.concept` tags:

```yaml
# models/marts/schema.yml
models:
  - name: dim_customer
    meta:
      concept: customer  # Just a string for now
    columns:
      - name: customer_id
        description: "Primary key"
```

You don't need a formal concept definition yet. Just tag what you're building.

---

### Step 3: Sync to Create Stubs

When you're ready to formalize, generate concept stubs:

#### Using the UI

1. Open dbt-conceptual
2. Click **Sync/Refresh**
3. Review the created stubs

#### Using the CLI

```bash
dcm sync --create-stubs

# Output:
# Scanning dbt models for meta.concept tags...
# Found 15 unique concepts referenced
# Created 15 concept stubs
# Created 8 relationship stubs (inferred from refs)
# 
# Run 'dcm status' to see what needs enrichment
```

---

### Step 4: Review What You Have

```bash
dcm status

# Output:
# Concepts: 15 total
#   - 0 fully enriched
#   - 15 stubs (missing: domain, owner)
#
# Coverage: 45/120 models (38%)
#   - Gold: 45/50 (90%)
#   - Silver: 0/40 (0%)
#   - Bronze: 0/30 (0%)
#
# Recommendations:
#   - Add domain and owner to concept stubs
#   - Consider adding taxonomy.yml for validation
```

---

### Step 5: Enrich Progressively

Now fill in the details:

#### Using the UI

1. Click on a concept in Canvas
2. Fill in the properties panel:
   - Domain
   - Owner
   - Description
   - Confidentiality (optional)
3. Save

#### Using YAML

The stub might look like this:

```yaml
# Generated stub
concepts:
  customer:
    name: "customer"
    domain: UNKNOWN
    owner: UNKNOWN
```

Enrich it:

```yaml
concepts:
  customer:
    name: "Customer"
    domain: party
    owner: commercial-analytics
    maturity: high
    description: |
      A party who has purchased products or services.
```

---

### Step 6: Add Governance When Ready

As your project matures, add governance controls:

```yaml
# dbt_project.yml
vars:
  dbt_conceptual:
    governance:
      require_domain: true   # Now enforced
      require_owner: true    # Now enforced
```

Add a taxonomy file when you want validation:

```yaml
# models/conceptual/taxonomy.yml
version: 1

confidentiality:
  - key: public
  - key: internal
  - key: confidential
```

---

## The UNKNOWN Pattern

Use `UNKNOWN` as an explicit placeholder:

```yaml
concepts:
  mystery_table:
    domain: UNKNOWN
    owner: UNKNOWN
```

**Why this works:**
- Gaps are visible, not hidden
- CI can warn (or error) on UNKNOWN
- Forces resolution before production
- Better than pretending it's documented

Configure how to handle it:

```yaml
vars:
  dbt_conceptual:
    governance:
      warn_on_unknown: true    # CI warns
      error_on_unknown: false  # CI doesn't fail (yet)
```

---

## Quick Wins First

Don't try to enrich everything at once. Prioritize:

| Priority | What | Why |
|----------|------|-----|
| 1 | Gold layer models | These feed dashboards |
| 2 | GDPR-relevant data | Compliance exposure |
| 3 | Frequently-asked-about tables | Reduces questions |
| 4 | Silver layer | Nice to have |
| 5 | Bronze/staging | Usually not needed |

---

## Timeline

| Day | Action |
|-----|--------|
| 0 | Add `meta.concept` tags to existing models |
| 1 | Run `dcm sync --create-stubs` |
| 2-5 | Enrich priority concepts (domain, owner) |
| Week 2 | Share with governance for review |
| Week 3 | Enable CI warnings |
| Month 1 | Enable CI enforcement for gold layer |

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Never getting around to enrichment | Schedule it. Put it in the sprint. |
| UNKNOWN becomes permanent | Set a deadline. CI can enforce. |
| Skipping governance review | They need to validate your domains/owners |
| Trying to cover everything | Gold layer first. Silver can wait. |

---

## Outcome

✓ Ship fast, formalize later  
✓ Concepts emerge from actual work  
✓ Progressive governance adoption  
✓ No big-bang documentation effort  
✓ Reality documented, not theory  

---

## Next Steps

- [Brownfield Adoption](brownfield-adoption.md) — If you have a large existing project
- [Working with Governance](working-with-governance.md) — When you're ready for review
- [Validation & Messages](../validation.md) — Understanding validation output
