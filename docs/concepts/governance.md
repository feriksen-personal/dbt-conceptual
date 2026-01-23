# Governance

{% hint style="info" %}
**Coming Soon** — Governance features are in development. See [GitHub Issue #22](https://github.com/dbt-conceptual/dbt-conceptual/issues/22) for progress.
{% endhint %}

## Governance-Ready, Not Governance-Replacement

A well-structured conceptual model provides the foundation for governance: domains, ownership, lineage, shared definitions. For many teams, this is more than they have today.

But dbt-conceptual is not a governance platform. It won't replace Collibra, Purview, or Alation. It feeds them.

### What You Get

| Capability | dbt-conceptual | Full Governance Platform |
|------------|----------------|--------------------------|
| Domain ownership | ✓ | ✓ |
| Concept definitions | ✓ | ✓ |
| Lineage (conceptual → physical) | ✓ | ✓ |
| Approval workflows | — | ✓ |
| Policy enforcement | — | ✓ |
| Cross-platform catalog | — | ✓ |
| Compliance reporting | — | ✓ |

### Where It Fits

**For teams without formal governance:**
This might be enough — and it's infinitely more than nothing. Domains, ownership, definitions, all versioned in git. That's a solid foundation.

**For teams on Databricks:**
The metadata structure aligns with Unity Catalog. Domains and ownership can feed your ABAC policies directly. Might be all you need.

**For teams with enterprise governance:**
dbt-conceptual becomes a feeder. Your conceptual model stays current in the codebase, then syncs to your catalog of record. Architecture that supports governance, not competes with it.

### Planned Features

- **Domain assignment** — Group concepts by business domain
- **Ownership metadata** — Link concepts to teams or individuals
- **Export to catalogs** — Push definitions to Collibra, Purview, Alation
- **Completeness rules** — Flag concepts missing required metadata

## The Bottom Line

If you need a full governance program, you need a full governance program.

But if you need shared vocabulary with clear ownership that actually stays current — and you're tired of the whiteboard being the last moment of truth — this gets you there.
