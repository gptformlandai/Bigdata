# Topic 004: JSON, CSV, XML, Avro, Parquet, ORC

## Goal

Know the common data file formats, when to use each one, and why format choice matters for Big Data performance.

## Simple Explanation

A file format is the way data is written to disk or sent over the network.

Some formats are easy for humans to read. Some are efficient for machines. Some are better for row-by-row events. Some are better for analytical queries over huge tables.

## Core Idea

- Definition: A data format defines how records, fields, types, and metadata are represented.
- Why it matters: Format affects storage size, schema safety, query speed, compatibility, and cost.
- Related terms: row format, columnar format, schema, compression, serialization.

## Format Comparison

| Format | Type | Human Readable | Schema Support | Best For |
|---|---|---:|---:|---|
| CSV | text, row-based | yes | weak | simple tables, exports |
| JSON | text, semi-structured | yes | weak unless enforced | APIs, logs, events |
| XML | text, semi-structured | yes | possible with XSD | legacy enterprise integrations |
| Avro | binary, row-based | no | strong | Kafka, streaming, schema evolution |
| Parquet | binary, columnar | no | strong | analytics, Spark, warehouses, lakes |
| ORC | binary, columnar | no | strong | Hive, high-performance analytics |

## How It Is Used

CSV:

- simple exchange format
- fragile with commas, quotes, newlines, and types

JSON:

- common for REST APIs and event logs
- flexible but can become inconsistent

XML:

- verbose but common in older enterprise systems
- still seen in banking, healthcare, insurance, and government integrations

Avro:

- compact binary row format
- popular with Kafka and Schema Registry
- good for evolving event schemas

Parquet:

- columnar format
- excellent for analytical queries
- supports predicate pushdown and column pruning

ORC:

- columnar format
- common in Hive ecosystems
- strong compression and indexing features

## Big Data / System Design Angle

For analytics, format choice can make a query cheap or painfully expensive.

Example: If a query only needs `customer_id` and `amount`, Parquet can read just those columns. CSV usually requires scanning and parsing whole rows.

General rule:

- APIs/events: JSON or Avro.
- Kafka with schema governance: Avro.
- Raw landing zone: JSON, Avro, or source-native format.
- Analytics tables: Parquet or ORC.
- Simple export: CSV.

## Example

JSON event:

```json
{"user_id":"u1","event_type":"click","page":"home"}
```

CSV row:

```csv
user_id,event_type,page
u1,click,home
```

Parquet is not readable directly, but analytically it behaves like:

```text
column user_id:    u1, u2, u3
column event_type: click, view, purchase
column page:       home, product, checkout
```

## Common Mistakes

- Mistake: Using CSV for everything.
- Better way: Use CSV for simple exchange, not large analytical pipelines.

- Mistake: Storing massive analytics tables as JSON.
- Better way: Convert curated data to Parquet or ORC.

- Mistake: Ignoring schema evolution.
- Better way: Use Avro, Parquet, or ORC with managed schemas for production datasets.

## Interview Speak

"For raw API events I may use JSON or Avro, but for large analytical tables I would choose Parquet or ORC because columnar storage reduces scan cost and improves compression. Avro is strong for streaming because it is compact and handles schema evolution well."

## Quick Recall

- One-liner: Text formats are easy to inspect; binary columnar formats are better for large analytics.
- Keywords: JSON, Avro, Parquet.
- Trap: Choosing a readable format when the real requirement is cheap distributed querying.
