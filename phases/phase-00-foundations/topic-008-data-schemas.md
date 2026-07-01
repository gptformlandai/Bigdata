# Topic 008: Data Schemas

## Goal

Understand schemas as data contracts that define what fields exist, what types they have, and what meaning consumers can rely on.

## Simple Explanation

A schema is like a form template.

It tells everyone what fields should exist and what kind of values are valid.

Example:

```text
order_id: string
amount: decimal
created_at: timestamp
status: string
```

## Core Idea

- Definition: A schema defines the structure, field names, data types, and sometimes rules for a dataset or message.
- Why it matters: Schemas let producers and consumers agree on data shape.
- Related terms: contract, data type, validation, schema registry, table definition.

## How It Is Used

Schemas appear in:

- SQL table definitions
- Avro schemas
- Protobuf messages
- JSON schema
- Parquet metadata
- API contracts
- data warehouse models

Example SQL schema:

```sql
CREATE TABLE orders (
    order_id VARCHAR,
    customer_id VARCHAR,
    amount DECIMAL(10, 2),
    status VARCHAR,
    created_at TIMESTAMP
);
```

## Big Data / System Design Angle

Schemas protect pipelines from silent breakage.

Without schemas:

- field names drift
- data types change unexpectedly
- downstream jobs fail
- dashboards become wrong
- ML features become unreliable

Schema-on-write:

- validate before storing
- common in warehouses and relational databases

Schema-on-read:

- store first, interpret later
- common in data lakes

Mature systems often combine both:

- raw layer may be flexible
- curated layer should be strongly modeled

## Example

Bad event:

```json
{"order_id": "o1", "amount": "forty dollars"}
```

Schema expects:

```text
amount: decimal
```

A validation layer should reject or quarantine this record.

## Common Mistakes

- Mistake: Saying JSON has no schema.
- Better way: JSON may not enforce schema by itself, but production systems can enforce JSON Schema or event contracts.

- Mistake: Treating schema as only field names.
- Better way: Include types, nullability, meaning, allowed values, and ownership.

- Mistake: Allowing everyone to change schemas freely.
- Better way: Use review, compatibility rules, and versioning.

## Interview Speak

"A schema is a contract between producers and consumers. It defines field names, types, nullability, and meaning. In a production data platform I would enforce schemas for important events and curated tables so downstream jobs, dashboards, and ML features do not silently break."

## Quick Recall

- One-liner: A schema is a contract for data shape and meaning.
- Keywords: fields, types, contract.
- Trap: Confusing flexible storage with schema-free ownership.
