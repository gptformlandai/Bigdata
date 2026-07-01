# Topic 266: Design Data Lake For An Enterprise

## 1. Goal

Design an enterprise data lake that stores data from many business domains and supports analytics, ML, governance, and long-term retention.

## 2. Baby Intuition

An enterprise data lake is a central storage campus.

Many teams bring data there, but the campus needs roads, signs, security, cleaning rules, and ownership.

## 3. Requirements

Clarify:

- Which sources are in scope: databases, files, streams, SaaS, logs?
- Is this lake for analytics, ML, archival, or all?
- What data sensitivity exists?
- Who owns datasets?
- Do we need lakehouse ACID tables?
- What cloud/on-prem constraints exist?

## 4. Functional Requirements

- ingest batch files, CDC, and streaming data
- store raw, cleaned, and business-ready data
- support schema evolution and table versioning
- catalog datasets and metadata
- enforce access control
- support BI, ML, ad hoc queries, and backfills
- track lineage, quality, and ownership

## 5. Non-Functional Requirements

- scalable and low-cost storage
- strong governance
- reliable ingestion
- data isolation by domain/sensitivity
- high query performance for common workloads
- disaster recovery and retention
- secure encryption and audit logging

## 6. Capacity Estimation

Example:

```text
500 source systems
average 100 GB/day/source
= 50 TB/day new raw data

with bronze/silver/gold copies:
total daily growth may be 2x to 4x raw size
```

Always estimate both raw data and derived data.

## 7. Events, APIs, And Interfaces

Ingestion interfaces:

- object storage file drop
- Kafka/Kinesis/Pub/Sub streams
- CDC connectors
- batch ETL jobs
- SaaS connectors

Consumer interfaces:

- SQL query engines
- Spark/Flink jobs
- notebooks
- ML training jobs
- BI tools

## 8. Data Model

Recommended layout:

```text
bronze/domain/source/table/ingest_date=YYYY-MM-DD/
silver/domain/entity/table_date=YYYY-MM-DD/
gold/domain/data_product/table_date=YYYY-MM-DD/
```

Table metadata:

```text
dataset_name
owner
domain
classification
schema
lineage
quality_rules
retention_policy
access_policy
```

## 9. High-Level Architecture

```text
sources
  -> ingestion layer
  -> bronze raw lake
  -> validation/cleaning
  -> silver curated lakehouse tables
  -> business transforms
  -> gold data products
  -> BI, ML, warehouse, APIs

catalog/governance/security/observability surround every layer
```

## 10. Data Flow

1. Source data arrives through batch, CDC, or stream ingestion.
2. Bronze stores raw immutable data.
3. Validation checks schema, freshness, and quality.
4. Silver tables standardize and clean entities.
5. Gold tables build business metrics and data products.
6. Catalog records schema, owner, lineage, and classifications.
7. Query engines and ML jobs consume governed datasets.
8. Retention and deletion workflows manage lifecycle.

## 11. Deep Dive Components

Lakehouse table format:

- supports ACID commits
- supports schema evolution
- supports time travel
- supports compaction

Catalog:

- dataset discovery
- ownership
- classification
- access request workflow
- lineage

Governance:

- RBAC/ABAC
- row/column policies
- masking/tokenization
- audit logs
- retention and deletion

## 12. Scaling And Partitioning

- Partition by date for large event tables.
- Avoid over-partitioning by high-cardinality columns.
- Use clustering/Z-order/sort for common filters.
- Compact small files.
- Separate compute clusters by workload/team.
- Use domain-based namespaces for organization.

## 13. Consistency And Correctness

- Use atomic table commits for curated tables.
- Keep bronze immutable for replay.
- Apply schema contracts for important sources.
- Track data quality checks.
- Publish only certified gold datasets to broad consumers.

## 14. Failure Handling

| Failure | Handling |
|---|---|
| source late | freshness alert and delayed publish |
| bad schema | quarantine data and notify owner |
| corrupt transform | time travel rollback and backfill |
| small files | compaction job |
| access misconfiguration | policy tests and audits |

## 15. Monitoring, Cost, And Security

Monitor:

- ingestion freshness
- table quality
- storage growth
- query cost
- compaction health
- access errors

Cost:

- tier cold data
- compact files
- prune partitions
- expire old snapshots
- chargeback/showback by domain/team

Security:

- encrypt data at rest/in transit
- classify sensitive data
- enforce least privilege
- mask/tokenize sensitive columns
- audit access

## 16. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| centralized lake | shared data platform | governance complexity |
| domain ownership | scalable ownership | standards needed |
| raw bronze retention | replay and audit | storage cost |
| lakehouse tables | ACID and performance | metadata/operations overhead |

## 17. Interview-Ready Final Answer

"I would design the enterprise lake as a governed lakehouse with bronze, silver, and gold layers. Batch, CDC, and stream ingestion write immutable raw data to bronze. Validation and standardization produce silver entities, and business transforms produce certified gold data products. A catalog tracks owner, schema, lineage, classification, and retention. Query engines, ML jobs, and BI consume governed tables. I would use ACID table formats, partitioning, compaction, schema contracts, data quality checks, access policies, audit logs, and cost controls such as tiering and chargeback."

## 18. Quick Recall

- One-line summary: Enterprise data lake is governed shared storage for raw, curated, and business-ready data.
- Core tools: object storage, Iceberg/Delta/Hudi, catalog, Spark/Flink, query engines, governance.
- Main trap: dumping files without ownership, quality, catalog, or security.
- Memory trick: storage campus with roads, signs, and guards.

