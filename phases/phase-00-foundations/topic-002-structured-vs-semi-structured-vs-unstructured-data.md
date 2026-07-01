# Topic 002: Structured vs Semi-Structured vs Unstructured Data

## Goal

Understand the three major shapes of data and how that shape affects storage, querying, processing, and system design choices.

## Simple Explanation

Think of data like information in containers.

- Structured data is like a spreadsheet: fixed columns, clear types, predictable rows.
- Semi-structured data is like a labeled form that can vary: JSON, XML, logs.
- Unstructured data is like raw content: images, PDFs, videos, audio, free text.

## Core Idea

- Definition: Data can be classified by how strictly its structure is defined.
- Why it matters: Structure determines how easily we can validate, query, compress, index, and process the data.
- Related terms: schema, rows, columns, documents, blobs, logs, metadata.

## The Three Types

| Type | Shape | Examples | Best Fit |
|---|---|---|---|
| Structured | Fixed rows and columns | SQL tables, CSV with fixed columns | transactions, reporting, dashboards |
| Semi-structured | Flexible fields with labels | JSON, XML, Avro, event logs | events, APIs, streaming |
| Unstructured | No fixed record schema | images, videos, PDFs, emails | search, ML, document processing |

## How It Is Used

Structured data:

- stored in relational databases or warehouses
- queried with SQL
- used for orders, payments, inventory, users, claims

Semi-structured data:

- common in APIs and event streams
- stored in document databases, Kafka topics, object storage, or lakehouse tables
- used for clickstream, logs, telemetry, nested events

Unstructured data:

- stored in object stores like S3, GCS, ADLS
- processed using search, ML, OCR, computer vision, or NLP pipelines
- used for videos, support tickets, medical images, PDFs

## Big Data / System Design Angle

- Structured data is easiest to query and validate.
- Semi-structured data is flexible but can become messy without schema governance.
- Unstructured data usually needs metadata and specialized processing before it becomes analytically useful.

Interview trigger words:

- "events" often means semi-structured data.
- "reports" often means structured data.
- "images, PDFs, videos, text corpus" often means unstructured data.

## Example

Structured:

```text
order_id,customer_id,amount,status
o1,c1,49.99,paid
```

Semi-structured:

```json
{
  "order_id": "o1",
  "customer": {
    "id": "c1",
    "region": "US"
  },
  "amount": 49.99,
  "status": "paid"
}
```

Unstructured:

```text
Customer uploaded a product review video.
```

The video is unstructured, but metadata around it can be structured:

```json
{
  "video_id": "v1",
  "user_id": "u7",
  "duration_seconds": 45,
  "uploaded_at": "2026-07-01T10:00:00Z"
}
```

## Common Mistakes

- Mistake: Treating JSON as automatically safe because it has field names.
- Better way: Use schemas or contracts for important JSON events.

- Mistake: Storing unstructured data without metadata.
- Better way: Store metadata like owner, timestamp, object type, source, retention, and access level.

- Mistake: Putting everything into relational tables.
- Better way: Match storage to access pattern and structure.

## Interview Speak

"I would first classify the data shape. Structured data is best for SQL and reporting, semi-structured data is common for APIs and events, and unstructured data like videos or PDFs usually needs object storage plus metadata and specialized processing. The choice affects schema validation, storage format, query engine, cost, and governance."

## Quick Recall

- One-liner: Data shape decides how easy it is to query, validate, and scale.
- Keywords: tables, JSON, blobs.
- Trap: Assuming flexible data means no schema is needed.
