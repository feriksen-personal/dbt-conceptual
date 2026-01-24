# Brownfield Adoption

**"We have 200 models and no governance."**

You're not starting from scratch. You need quick wins and progressive adoption.

![Brownfield adoption timeline](../../assets/workflow-brownfield-adoption.svg)

---

## When to Use This Approach

- Existing dbt project with many models
- Governance pressure (audit, compliance, new hire asking questions)
- Can't stop everything to document
- Need to show progress, not perfection
- Tribal knowledge scattered across the team

---

## The Reality

You can't document everything at once. You shouldn't try.

**The goal:** Progressive coverage. Show improvement. Prioritize by risk.

---

## The Workflow

### Day 0: See What You Have

#### Using the UI

1. Open dbt-conceptual
2. Click **Sync/Refresh**
3. Review the notification:
   ```
   ✓ Found 45 models with meta.concept tags
   + Created 12 concept stubs
   + Created 8 relationship stubs
   ```

#### Using the CLI

```bash
dcm sync --create-stubs

# Output:
# Scanning manifest.json...
# Found 200 models total
# Found 45 with meta.concept tags
# Created 12 concept stubs
# Created 8 relationship stubs
# 
# Run 'dcm status' to see coverage
```

**Even if you have no `meta.concept` tags yet**, the sync will analyze your model names and suggest potential concepts.

---

### Day 1: Assess the Gaps

```bash
dcm status

# Output:
# ┌─────────────────────────────────────────────────────┐
# │  Coverage Summary                                    │
# ├─────────────────────────────────────────────────────┤
# │  Gold layer:    12/50 models   (24%)               │
# │  Silver layer:   0/80 models   (0%)                │
# │  Bronze layer:   0/70 models   (0%)                │
# │                                                     │
# │  Concepts: 12 stubs (0 enriched)                   │
# │  Missing: domain (12), owner (12)                  │
# └─────────────────────────────────────────────────────┘
```

Or in the UI, check the **Coverage View** for a visual breakdown.

---

### Day 2: Prioritize

Not all models are equal. Prioritize by:

| Priority | Criteria | Why |
|----------|----------|-----|
| **Critical** | GDPR/PII data | Compliance risk |
| **Critical** | Executive dashboards | Visibility |
| **High** | Frequently queried | High impact |
| **High** | Recent incidents | Known pain |
| **Medium** | Core dimensions | Foundation |
| **Low** | Staging/bronze | Internal only |

**Start with one domain.** Finance, Customer, or whatever has the most pressure.

---

### Week 1: Enrich Priority Domain

Pick your priority domain and fully document it:

```yaml
# models/conceptual/conceptual.yml
domains:
  finance:
    name: "Finance"
    owner: finance-analytics
    steward: data-governance

concepts:
  revenue:
    name: "Revenue"
    domain: finance
    owner: finance-analytics
    maturity: high
    confidentiality: confidential
    description: |
      Recognized revenue from customer transactions.
      Source of truth for financial reporting.

  cost:
    name: "Cost"
    domain: finance
    owner: finance-analytics
    maturity: high
    description: |
      Direct and indirect costs associated with operations.
```

Tag the corresponding models:

```yaml
# models/marts/finance/schema.yml
models:
  - name: fct_revenue
    meta:
      concept: revenue
  - name: fct_costs
    meta:
      concept: cost
```

**Check progress:**
```bash
dcm status --domain finance
# Finance: 8/8 models covered (100%)
```

---

### Week 2: Share with Governance

Share your progress:

```bash
# Export for review
dcm export --format html --output governance-review.html
```

Or share the Git link:
```
https://github.com/your-org/repo/blob/main/models/conceptual/conceptual.yml
```

Get feedback. Iterate. Move to the next domain.

---

### Month 1: Enable CI (Soft)

Start with warnings, not errors:

```yaml
# dbt_project.yml
vars:
  dbt_conceptual:
    governance:
      # Warnings only
      warn_on_uncovered_gold_models: true
      warn_on_unknown: true
      
      # Not yet enforced
      require_domain: false
      require_owner: false
```

CI output:
```
⚠ Warning: 8 gold models without concept tags
⚠ Warning: 3 concepts with UNKNOWN domain
✓ Coverage: 72% (target: 80%)
```

---

### Month 2-3: Tighten Progressively

As coverage improves, enable enforcement:

```yaml
# Month 2: Require basics
vars:
  dbt_conceptual:
    governance:
      require_domain: true
      require_owner: true
      warn_on_uncovered_gold_models: true

# Month 3: Full enforcement
vars:
  dbt_conceptual:
    governance:
      require_domain: true
      require_owner: true
      error_on_uncovered_gold_models: true
      enforce_taxonomy_validation: true
```

---

## Progressive Strictness

| Phase | Coverage | CI Behavior |
|-------|----------|-------------|
| Week 1 | ~25% | No validation |
| Week 2 | ~40% | Warnings only |
| Month 1 | ~60% | Warnings, block on critical |
| Month 2 | ~80% | Errors on gold layer |
| Month 3+ | ~90% | Full enforcement |

---

## The Coverage Dashboard

Track your progress over time:

```bash
dcm coverage --trend

# Output:
# Week 1:  ████░░░░░░░░░░░░░░░░  22%
# Week 2:  ████████░░░░░░░░░░░░  38%
# Week 3:  ████████████░░░░░░░░  55%
# Week 4:  ████████████████░░░░  72%
# Week 5:  ██████████████████░░  85%
```

Show this to your governance office. Progress is visible.

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Trying to cover everything at once | One domain at a time |
| Skipping governance review | They'll find issues later |
| CI fails on day one | Start with warnings |
| UNKNOWN becomes permanent | Set deadlines, CI can enforce |
| Team doesn't adopt | Make it part of PR checklist |

---

## Team Adoption Tips

Make it stick:

1. **PR Template:** Add "Concept tagged?" to your PR checklist
2. **Code Review:** Reviewers check for `meta.concept` on new models
3. **Sprint Goal:** "Finance domain 100% covered by Friday"
4. **Celebrate:** Share coverage milestones in Slack

---

## Outcome

✓ Quick wins in the first week  
✓ Progress visible to governance  
✓ No big-bang effort required  
✓ CI enforces standards automatically  
✓ Coverage improves with every PR  

---

## Next Steps

- [Working with Governance](working-with-governance.md) — The collaboration handshake
- [CI/CD Integration](../ci-integration.md) — Detailed pipeline setup
- [Validation & Messages](../validation.md) — Understanding validation output
