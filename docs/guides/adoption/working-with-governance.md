# Working with Governance

**The collaboration handshake.**

Governance wants visibility. You want to ship. dbt-conceptual bridges the gap.

![Governance collaboration workflow](../../assets/workflow-governance-collaboration.svg)

---

## The Reality

Traditional governance:
- "Fill out this form"
- "Attend the review meeting"  
- "Update the catalog manually"
- "Wait for approval"

**dbt-conceptual governance:**
- Share a link
- Async review
- CI validates
- Tags flow automatically

---

## The Collaboration Pattern

### Step 1: Data Team Creates Draft

Create your conceptual model with best-guess values:

```yaml
# models/conceptual/conceptual.yml
concepts:
  customer:
    name: "Customer"
    domain: party          # Best guess
    owner: commercial-analytics
    description: |
      A party who purchases products or services.
```

Or use explicit placeholders:

```yaml
concepts:
  customer:
    domain: UNKNOWN        # Need governance input
    owner: UNKNOWN         # Need governance input
```

---

### Step 2: Share for Review

**Option A: Git Link**

Send the direct link to your conceptual.yml:
```
https://github.com/your-org/repo/blob/feature-branch/models/conceptual/conceptual.yml
```

**Option B: Pull Request**

Create a PR and request review from governance:
```
PR: Add conceptual model for Customer domain
Reviewers: @governance-team
```

**Option C: Export**

Generate a shareable document:
```bash
dcm export --format html --output model-for-review.html
dcm export --format pdf --output model-for-review.pdf
```

**Option D: UI Access**

Give governance read access to the dbt-conceptual UI. They can review visually without touching YAML.

---

### Step 3: Governance Reviews

Governance office checks:

| Check | Question |
|-------|----------|
| **Domains** | Do these match our enterprise domain model? |
| **Owners** | Are these the right accountable parties? |
| **Vocabulary** | Do terms align with our glossary? |
| **Classification** | Is confidentiality appropriate? |
| **Completeness** | Are key entities missing? |

They provide feedback via:
- PR comments
- Email
- Shared document annotations
- Direct YAML edits (if they're comfortable)

---

### Step 4: Iterate

Update based on feedback:

```yaml
# Before (data team guess)
concepts:
  customer:
    domain: commercial
    owner: sales-team

# After (governance feedback)
concepts:
  customer:
    domain: party           # Corrected: party is the standard domain
    owner: commercial-analytics  # Corrected: proper owner
    steward: data-governance     # Added: governance contact
```

---

### Step 5: Align Taxonomy

Share your taxonomy.yml for vocabulary alignment:

```yaml
# models/conceptual/taxonomy.yml
version: 1

confidentiality:
  - key: public
    brief: "No restrictions"
  - key: internal
    brief: "Employees only"
  - key: confidential
    brief: "Need-to-know"

regulatory:
  - key: GDPR
    brief: "EU data protection"
  - key: SOX
    brief: "Financial controls"
```

Governance validates:
- Keys match enterprise standards
- Descriptions are accurate
- Nothing critical is missing

---

### Step 6: Approve and Enforce

Once approved:

1. **Merge the PR** — Conceptual model is now in main branch
2. **Enable CI validation** — New changes must comply
3. **Tags flow to UC** — Unity Catalog updated automatically

```yaml
# dbt_project.yml (post-approval)
vars:
  dbt_conceptual:
    governance:
      require_domain: true
      require_owner: true
      enforce_taxonomy_validation: true
```

---

## What Governance Gets

Without extra work from governance, they get:

| Capability | How |
|------------|-----|
| **Domain ownership map** | From conceptual.yml |
| **Coverage reports** | `dcm coverage` or Coverage View |
| **Change visibility** | Git history, PR reviews |
| **Compliance tracking** | Taxonomy validation in CI |
| **Catalog integration** | Tags propagate to Unity Catalog |

**No spreadsheets. No manual updates. No "please update the catalog."**

---

## What Governance Still Owns

dbt-conceptual doesn't replace governance. It feeds it.

| Governance owns | dbt-conceptual provides |
|-----------------|------------------------|
| Column-level classification (PII/PHI) | Entity-level metadata |
| Access control / RLS | Ownership information for policies |
| Compliance reporting | Coverage data, tag propagation |
| Enterprise glossary | Links to glossary terms |
| Policy enforcement | Metadata to inform policies |

---

## The Handoff

**dbt-conceptual provides:**
- Business context
- Ownership
- Domains
- Maturity levels
- Glossary links
- High-level classification

**Your governance tooling handles:**
- Granular classification
- Enforcement
- Access control
- Audit
- Compliance reporting

---

## Tips for Success

### For Data Teams

- **Engage early** — Don't wait until audit time
- **Use UNKNOWN** — Explicit gaps are better than wrong values
- **Small PRs** — One domain at a time is easier to review
- **Document rationale** — PR descriptions help governance understand

### For Governance Office

- **Review async** — Don't require meetings for every change
- **Trust but verify** — CI validates ongoing compliance
- **Start permissive** — Enable strictness progressively
- **Celebrate progress** — Coverage trending up is a win

---

## Governance as Code

The ultimate goal:

![CI governance validation](../../assets/workflow-ci-governance.svg)

**Governance validated on every PR. No manual review required.**

- Push code → CI checks governance compliance
- Pass → Merge allowed
- Fail → Fix before merge

Governance becomes part of the development workflow, not a separate process.

---

## Common Concerns

| Concern | Response |
|---------|----------|
| "Data teams will get it wrong" | That's why we review. And CI catches drift. |
| "We need approval workflows" | Use PR reviews. Same result, Git-native. |
| "This won't scale" | It scales better than spreadsheets. |
| "What about column-level?" | Use your existing tools. We handle entity-level. |

---

## Outcome

✓ Shared vocabulary between data and governance  
✓ Async collaboration via Git  
✓ Visibility without burden  
✓ CI enforces standards automatically  
✓ Governance embedded in development workflow  

---

## Next Steps

- [CI/CD Integration](../ci-integration.md) — Detailed pipeline setup
- [Validation & Messages](../validation.md) — Understanding validation output
- [Governance](../../core-concepts/governance.md) — Full governance feature reference
