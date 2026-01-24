# Choosing Your Approach

Every team starts somewhere different. This guide helps you pick the right adoption path.

## Signs You Need This

You're in the right place if:

- An audit is coming and someone asked "where's your data catalog?"
- GDPR/SOC2 compliance is on the roadmap
- A new governance hire keeps asking "who owns this table?"
- An incident got traced back to "nobody knew who owned that pipeline"
- Your team has grown and tribal knowledge isn't scaling
- You're tired of the whiteboard being the last moment of truth

If any of these resonate — read on.

---

## The Decision Matrix

| You have... | You need... | Recommended approach |
|-------------|-------------|---------------------|
| New project, clear requirements | Governance alignment from day one | [Top-Down: Conceptual First](greenfield-top-down.md) |
| New project, still exploring | Fast iteration, formalize later | [Bottom-Up: Models First](greenfield-bottom-up.md) |
| Existing project, governance pressure | Quick wins, progressive adoption | [Brownfield Adoption](brownfield-adoption.md) |
| Existing project, proactive cleanup | Systematic coverage improvement | [Brownfield Adoption](brownfield-adoption.md) |
| Any project, need governance buy-in | Collaborative vocabulary alignment | [Working with Governance](working-with-governance.md) |

---

## Two Directions, One Sync

dbt-conceptual supports bi-directional sync between concepts and models:

![Bi-directional sync](../../assets/workflow-bi-directional-sync.svg)

### Top-Down

```
Define concepts → Tag models → Validate coverage
```

You know what you're building. Define the business entities first, then link your dbt models to them.

**Best for:** Regulated industries, clear domain model, governance engaged early.

### Bottom-Up

```
Build models → Sync/create stubs → Enrich concepts
```

You're iterating fast. Build your models, add `meta.concept` tags as you go, then generate concept stubs and enrich them.

**Best for:** Startups, exploratory projects, brownfield adoption.

---

## The Files

![File structure](../../assets/file-structure.svg)

| File | Required | Contains |
|------|----------|----------|
| `conceptual.yml` | Yes | Concepts, relationships, domains, owners |
| `taxonomy.yml` | No | Validation rules for confidentiality, retention, etc. |

**No taxonomy file?** That's fine — free text is allowed everywhere. Add taxonomy when you're ready for validation. Governance scales with your maturity.

---

## Quick Comparison

| Aspect | Top-Down | Bottom-Up |
|--------|----------|-----------|
| Starting point | conceptual.yml | dbt models |
| First artifact | Conceptual model | Working pipeline |
| Governance alignment | Upfront | Iterative |
| Risk of rework | Lower | Higher (but faster start) |
| Best for | Compliance-driven | Delivery-driven |

---

## The Bi-Directional Workflow

Regardless of where you start, both directions stay in sync:

### Using the UI

1. Open dbt-conceptual
2. Click **Sync/Refresh**
3. Changes flow both ways:
   - New concepts appear on canvas
   - New `meta.concept` tags create stubs

### Using the CLI

```bash
# Create stubs from existing meta.concept tags
dcm sync --create-stubs

# Output:
# Created 12 concept stubs
# Created 8 relationship stubs
# Run 'dcm status' to see what needs enrichment
```

---

## What Success Looks Like

| Timeframe | Milestone |
|-----------|-----------|
| Day 1 | Stubs created, gaps visible |
| Week 1 | Priority domain mapped (e.g., Finance) |
| Week 2 | Governance office reviewed and approved |
| Month 1 | Gold layer 80% covered |
| Month 3 | CI enforcing coverage, tags flowing to UC |
| Ongoing | Governance lives in code, updated with every PR |

---

## Next Steps

Pick your path:

- **Starting fresh?** → [Top-Down: Conceptual First](greenfield-top-down.md)
- **Have existing models?** → [Bottom-Up: Models First](greenfield-bottom-up.md) or [Brownfield Adoption](brownfield-adoption.md)
- **Need governance buy-in?** → [Working with Governance](working-with-governance.md)
