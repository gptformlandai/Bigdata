# Phase 0 Review: Computer Science And Data Foundations

This review checks whether the foundations are strong enough to move into Big Data basics.

## Phase Summary

Phase 0 covered the building blocks behind data systems:

- data shapes and file formats
- schemas, schema evolution, encoding, and serialization
- Linux, networking, APIs, and SQL
- indexes, transactions, ACID, CAP, consistency, latency, throughput, and scaling

The main idea:

```text
Big Data is not just tools. It is data representation + movement + correctness + scale.
```

## Checkpoint 1: Topics 001-005

Topics:

- What is data?
- Structured vs semi-structured vs unstructured data
- Files, records, rows, columns
- JSON, CSV, XML, Avro, Parquet, ORC
- Compression

### Quiz

1. What is the difference between data and information?
2. Why is semi-structured data common in event pipelines?
3. Why is Parquet usually better than CSV for analytical queries?
4. What problem does compression solve?
5. Why can too many small files hurt Big Data systems?

### Practical Exercise

Take a sample order dataset and represent it in:

- CSV
- JSON
- a simple table schema

Then explain which format you would use for:

- API response
- Kafka event
- warehouse table
- one-time export

### Mini System Design Question

> You receive 5 TB/day of clickstream logs. What file format and compression would you choose for raw storage and analytical querying?

Strong direction:

- Raw events can land as JSON or Avro.
- Curated analytics should usually use Parquet or ORC.
- Use compression such as snappy or zstd depending on speed and cost requirements.

### Recap Table

| Concept | Must Remember |
|---|---|
| Data | recorded fact |
| Structured data | fixed rows and columns |
| Semi-structured data | flexible fields like JSON |
| Unstructured data | raw content like images or PDFs |
| Parquet/ORC | columnar analytics formats |
| Compression | saves storage/network, costs CPU |

## Checkpoint 2: Topics 006-010

Topics:

- Serialization and deserialization
- Encoding
- Data schemas
- Schema evolution
- Basic Linux for data engineering

### Quiz

1. What is serialization?
2. Why is UTF-8 a common default?
3. What does a schema protect?
4. Which schema changes are usually safe?
5. Which Linux commands help inspect huge files safely?

### Practical Exercise

Create a sample JSON event and define:

- required fields
- optional fields
- data types
- one safe schema evolution
- one breaking schema evolution

### Mini System Design Question

> You own a Kafka event used by five teams. Product wants to add a new field. How do you evolve the schema safely?

Strong direction:

- Add optional field or default.
- Register schema.
- Keep backward compatibility.
- Do not rename or delete fields casually.
- Monitor consumers after rollout.

### Recap Table

| Concept | Must Remember |
|---|---|
| Serialization | object to bytes |
| Deserialization | bytes to object |
| Encoding | character/value to bytes |
| Schema | data contract |
| Schema evolution | safe contract change |
| Linux | practical debugging layer |

## Checkpoint 3: Topics 011-015

Topics:

- Networking basics
- APIs and REST
- SQL basics
- Indexes
- Transactions

### Quiz

1. What does DNS do?
2. Why should network calls have timeouts?
3. What does HTTP `429` mean?
4. Why can an index slow down writes?
5. Why should a money transfer use a transaction?

### Practical Exercise

Design a tiny API ingestion job:

- call a paginated API
- handle `429` with retry delay
- write raw responses
- transform into a SQL table
- deduplicate by id

### Mini System Design Question

> You need to ingest customer records from a third-party REST API every hour. What failure cases do you design for?

Strong direction:

- pagination
- rate limits
- retries with backoff
- auth failures
- schema changes
- duplicate records
- partial ingestion
- monitoring and alerting

### Recap Table

| Concept | Must Remember |
|---|---|
| DNS | name to IP |
| HTTP | request/response protocol |
| REST | resource-based API style |
| SQL | table query language |
| Index | faster reads, slower writes |
| Transaction | all-or-nothing unit |

## Checkpoint 4: Topics 016-020

Topics:

- ACID
- CAP theorem
- Consistency models
- Latency vs throughput
- Horizontal vs vertical scaling

### Quiz

1. What does each ACID letter mean?
2. What is the real CAP trade-off during a partition?
3. When is eventual consistency acceptable?
4. What is the difference between latency and throughput?
5. Why is horizontal scaling harder than vertical scaling?

### Practical Exercise

For each feature, choose consistency and scaling strategy:

- bank account balance
- social media like count
- product recommendation
- inventory reservation
- daily analytics dashboard

### Mini System Design Question

> You are designing a multi-region profile service. Users should see their own profile updates immediately, but other users can see stale data for a few seconds. What consistency model fits?

Strong direction:

- Use read-your-writes for the editing user.
- Allow eventual consistency for other users.
- Replicate asynchronously if business allows.
- Monitor replication lag.

### Recap Table

| Concept | Must Remember |
|---|---|
| ACID | transaction reliability |
| CAP | during partition, choose C or A |
| Consistency model | when reads see writes |
| Latency | time for one operation |
| Throughput | operations/data per time |
| Horizontal scaling | add machines |
| Vertical scaling | bigger machine |

## Must-Know Concepts

You should be comfortable explaining:

- data vs information
- structured vs semi-structured vs unstructured data
- row-based vs columnar formats
- schema and schema evolution
- serialization vs encoding
- SQL query basics
- why indexes are not free
- transaction and ACID basics
- CAP theorem nuance
- strong vs eventual consistency
- latency vs throughput
- scale up vs scale out

## Common Interview Questions

1. Why would you store analytical data in Parquet instead of CSV?
2. How do you safely evolve a Kafka event schema?
3. What happens if a REST API returns duplicate records during retry?
4. How does an index improve reads and hurt writes?
5. Why are distributed transactions hard?
6. Explain ACID with a banking example.
7. Explain CAP theorem without saying "pick any two."
8. When would you choose eventual consistency?
9. How do you reduce p99 latency?
10. When would you scale vertically vs horizontally?

## Hands-On Project

Build a mini local data pipeline.

### Requirements

Use a small orders dataset with fields:

```text
order_id, customer_id, amount, status, created_at
```

### Steps

1. Create raw data in JSON.
2. Validate records against a simple schema.
3. Quarantine bad records.
4. Convert valid records into CSV.
5. Run SQL-style aggregations using SQLite or Python.
6. Calculate revenue by day and customer.
7. Add a schema change: `currency`.
8. Explain whether the change is backward compatible.

### What This Teaches

- raw vs curated data
- validation
- schema thinking
- format conversion
- SQL aggregation
- bad-record handling
- simple evolution

## Production Checklist

Before moving data into production, ask:

- What is the source?
- What is the schema?
- What fields are required?
- What format is used?
- Is the data compressed?
- What encoding is expected?
- How do we handle malformed records?
- How do we handle duplicates?
- How do we evolve schema safely?
- Who owns the dataset?
- What is the retention policy?
- Is there PII or PHI?
- What are freshness requirements?
- What are latency and throughput targets?
- What consistency does the user need?
- How does the system scale?
- What is monitored?

## Final Phase 0 Interview Answer

"Before choosing Big Data tools, I clarify the data itself: its shape, schema, format, volume, freshness, correctness requirements, and consumers. Then I choose storage and processing patterns based on access needs. For analytics I prefer columnar formats like Parquet with compression. For events I care about serialization, schema evolution, and idempotency. For serving systems I reason about SQL, indexes, transactions, ACID, consistency, latency, throughput, and scaling. These foundations drive the architecture."
