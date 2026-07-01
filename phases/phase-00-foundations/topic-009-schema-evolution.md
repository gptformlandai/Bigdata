# Topic 009: Schema Evolution

## Goal

Understand how schemas change safely over time without breaking old data or active consumers.

## Simple Explanation

Systems change. New fields get added. Old fields become unused. Data types need fixes.

Schema evolution is the discipline of changing data contracts without breaking everything downstream.

## Core Idea

- Definition: Schema evolution is the controlled process of modifying schemas while preserving compatibility.
- Why it matters: Producers and consumers are often deployed at different times and old data still exists.
- Related terms: backward compatibility, forward compatibility, versioning, migration, default values.

## Compatibility Types

| Type | Meaning | Example |
|---|---|---|
| Backward compatible | new reader can read old data | add optional field with default |
| Forward compatible | old reader can read new data | add field old reader can ignore |
| Full compatible | both old and new readers work | safe additive changes |
| Breaking change | consumers may fail | rename required field, change type |

## Safe Changes

Usually safe:

- add optional fields
- add fields with defaults
- add enum values only if consumers tolerate unknowns
- deprecate fields before removing them

Risky or breaking:

- rename fields
- delete fields
- change `string` to `int`
- change meaning of a field without changing the name
- make optional fields required

## Big Data / System Design Angle

Schema evolution is critical in Kafka, data lakes, warehouses, APIs, and ML feature stores.

Why:

- old events may be replayed years later
- multiple teams consume the same data
- batch jobs may read historical partitions
- streaming jobs may fail on unexpected fields

Typical production approach:

1. Define compatibility rules.
2. Register schemas in a schema registry or catalog.
3. Add fields in a backward-compatible way.
4. Deploy consumers before producers for breaking migrations.
5. Backfill or migrate old data when required.
6. Monitor failures and data quality.

## Example

Version 1:

```json
{
  "order_id": "string",
  "amount": "decimal"
}
```

Version 2, safe additive change:

```json
{
  "order_id": "string",
  "amount": "decimal",
  "currency": "string, default USD"
}
```

Breaking change:

```json
{
  "id": "string",
  "amount_cents": "int"
}
```

The breaking version renamed fields and changed meaning.

## Common Mistakes

- Mistake: Renaming fields casually.
- Better way: Add the new field, write both for a while, migrate consumers, then remove later.

- Mistake: Changing type without a migration plan.
- Better way: Add a new field with the new type.

- Mistake: Assuming old data disappears.
- Better way: Design readers to handle historical schema versions.

## Interview Speak

"I would treat schemas as versioned contracts. Safe evolution usually means additive optional fields with defaults. Renames, deletes, and type changes are breaking, so I would use compatibility checks, a schema registry, staged rollout, backfills, and monitoring."

## Quick Recall

- One-liner: Schema evolution lets data contracts change without breaking consumers.
- Keywords: compatibility, versioning, defaults.
- Trap: Renaming a field instead of adding and migrating.
