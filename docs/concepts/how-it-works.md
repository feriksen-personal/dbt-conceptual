# How It Works

dbt-conceptual connects your conceptual model to your dbt implementation through metadata tags and YAML definitions.

## The Core Model

### Concepts

A concept represents a business entity — something meaningful to your organization that persists across technology changes.

```yaml
concepts:
  customer:
    name: "Customer"
    domain: party
    owner: customer_team
    definition: "A person or company that purchases products"
```

### Relationships

Relationships define how concepts connect. They use a verb-based naming convention.

```yaml
relationships:
  - name: places
    from: customer
    to: order
    cardinality: "1:N"
    definition: "A customer places one or more orders"
```

The relationship identifier becomes `customer:places:order`.

### Domains

Domains group related concepts. They help organize large models and assign ownership.

```yaml
domains:
  party:
    name: "Party"
    owner: party_team
  transaction:
    name: "Transaction"
    owner: orders_team
```

## Linking to dbt

### Concepts to Dimensions

Tag dimension models with `meta.concept`:

```yaml
models:
  - name: dim_customer
    meta:
      concept: customer
```

### Facts and Bridges

Facts and bridges are also concepts. Tag them with `meta.concept`:

```yaml
models:
  - name: fct_orders
    meta:
      concept: Order

  - name: bridge_customer_policy
    meta:
      concept: CustomerPolicy
```

Relationships between these concepts are defined in `conceptual.yml`:

```yaml
relationships:
  - name: places
    from: Customer
    to: Order
    cardinality: "1:N"

  - name: has
    from: Customer
    to: CustomerPolicy
    cardinality: "1:N"

  - name: covers
    from: CustomerPolicy
    to: Policy
    cardinality: "N:1"
```

This approach surfaces bridge tables as explicit concepts, connected via 1:N relationships rather than hidden N:M associations.

## Status Logic

### Concept Status

| Status | Condition |
|--------|-----------|
| `complete` | Has domain AND has implementing models |
| `draft` | Has domain but no implementing models |
| `stub` | No domain (created from sync) |
| `deprecated` | Has `replaced_by` set |

### Relationship Status

| Status | Condition |
|--------|-----------|
| `complete` | Both concepts have domains |
| `draft` | One or both concepts missing domain |
| `stub` | Missing verb |

## The Sync Process

When you run `dcm sync` or use the UI:

1. **Scan dbt project** — Find all models with `meta.concept`
2. **Match to definitions** — Link tagged models to defined concepts
3. **Identify gaps** — Find references that don't exist
4. **Create stubs** (optional) — Auto-generate placeholders for undefined concepts

## Layer Detection

Models are classified by their path:

| Layer | Detection | Editable |
|-------|-----------|----------|
| **Gold** | Path matches `gold_paths` config | Yes |
| **Silver** | Path matches `silver_paths` config | Yes |
| **Bronze** | Inferred from lineage | No (read-only) |

Default paths:
- Silver: `models/staging`, `models/silver`
- Gold: `models/marts`, `models/gold`

## Next Steps

- [Layer Model](layer-model.md) — Deep dive into the medallion architecture
- [Defining Concepts](../guides/defining-concepts.md) — Best practices for writing definitions
