# Tagging dbt Models

How to link your dbt models to conceptual model definitions.

## The Tag

Use `meta.concept` to link any dbt model to a concept:

```yaml
models:
  - name: dim_customer
    meta:
      concept: Customer
```

That's it. Dimensions, facts, bridges — they're all concepts. Tag with `meta.concept` and dbt-conceptual handles the rest.

## Tag Placement

Tags go in your model's YAML file, typically `schema.yml` or a dedicated model YAML.

```yaml
# models/gold/schema.yml
version: 2

models:
  - name: dim_customer
    description: "Customer dimension"
    meta:
      concept: Customer
    columns:
      - name: customer_key
        description: "Surrogate key"
```

## Dimensions

Dimensions implement a single concept. They answer "What is X?"

```yaml
# dim_customer implements the Customer concept
- name: dim_customer
  meta:
    concept: Customer

# dim_product implements the Product concept
- name: dim_product
  meta:
    concept: Product
```

One concept can have multiple implementing dimensions:

```yaml
# Both implement Customer
- name: dim_customer
  meta:
    concept: Customer

- name: dim_customer_snapshot
  meta:
    concept: Customer
```

## Facts and Bridges

Facts and bridges are also concepts. They represent business events or associations.

```yaml
# Order is a concept (the event of ordering)
- name: fct_orders
  meta:
    concept: Order

# CustomerPolicy is a bridge concept (the association between customer and policy)
- name: bridge_customer_policy
  meta:
    concept: CustomerPolicy
```

The relationships between these concepts are defined in your conceptual model:

```yaml
# In conceptual.yml
concepts:
  Customer:
    name: Customer
  Order:
    name: Order
  CustomerPolicy:
    name: Customer Policy

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

This replaces N:M relationships with explicit bridge concepts connected via 1:N relationships.

## Silver Layer

Silver models can also be tagged:

```yaml
# models/silver/schema.yml
models:
  - name: stg_customers
    meta:
      concept: Customer

  - name: stg_orders
    meta:
      concept: Order
```

This shows which concepts have staging implementations.

## Validation

After tagging, validate your model:

```bash
dcm validate
```

Common issues:
- **Unknown concept reference** — Concept doesn't exist in conceptual.yml
- **Orphan model** — Model in silver/gold path without tags

## Best Practices

1. **Tag early** — Add meta tags when creating new models
2. **One concept per model** — Keep models focused
3. **Bridge concepts are concepts** — Don't think of them differently
4. **Use stubs for discovery** — `dcm sync --create-stubs` finds untagged models
