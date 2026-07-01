# Topic 138: Data Lakehouse Architecture

## 1. Goal

Understand what a data lakehouse is, why it exists, and how its main layers fit together.

## 2. Baby Intuition

A raw data lake is like a huge storage room where everyone drops boxes.

A lakehouse is the same storage room, but now every box has a label, a catalog entry, access rules, version history, and a checkout system so people do not overwrite each other.

## 3. What It Is

- Simple definition: A lakehouse is a data lake with table management features that make it feel more reliable and query-friendly.
- Technical definition: A data lakehouse stores data files in distributed/object storage and uses a table format plus catalog metadata to provide transactions, schema management, time travel, and efficient analytics.
- Category: Modern analytical data platform architecture.
- Related terms: data lake, warehouse, object storage, Parquet, Iceberg, Delta Lake, Hudi, catalog, Spark, Trino.

## 4. Why It Exists

Traditional data lakes were cheap and flexible, but they had painful problems:

- too many raw files
- no reliable transactions
- readers could see half-written data
- schema changes could break jobs
- upserts/deletes were hard
- performance depended heavily on file layout
- governance and discovery were weak

Warehouses solved many of these problems, but they could be more expensive, more closed, or less flexible for raw/semi-structured data.

The lakehouse exists to bring warehouse-like reliability to open data lake storage.

## 5. Where It Fits In A Data Platform

```text
Sources
  -> ingestion/streaming
  -> object storage: S3/GCS/ADLS/HDFS
  -> lakehouse table format: Iceberg/Delta/Hudi
  -> catalog/metastore
  -> compute engines: Spark/Flink/Trino/Presto/Databricks
  -> BI/ML/reports/products
```

The lakehouse is usually the central analytical storage layer.

## 6. How It Works Step By Step

1. Raw data lands in object storage as files.
2. A writer job converts or appends data into optimized files, often Parquet.
3. A table format records which files belong to the table.
4. The table format commits a new table snapshot/version.
5. Query engines ask the catalog where the table metadata lives.
6. Readers load the current snapshot and scan only the needed files.
7. Maintenance jobs compact files, clean old versions, and optimize layout.

Important idea:

```text
The data files are not enough.
The metadata decides what the table means right now.
```

## 7. How To Use It Practically

Common practical flow:

```text
Kafka/CDC/files
  -> Spark/Flink ingestion job
  -> Iceberg/Delta/Hudi table in S3
  -> Trino/Spark/Databricks queries
  -> dashboards, ML features, reporting
```

Typical table layers:

| Layer | Meaning |
|---|---|
| bronze/raw | minimally cleaned source data |
| silver/clean | deduped, typed, joined, reliable data |
| gold/business | aggregates and business-ready tables |

## 8. Real-World Scenario

- Product/system: E-commerce analytics platform.
- Problem: Clicks, orders, payments, inventory, and refunds arrive from many systems.
- How lakehouse helps: Store raw events cheaply, clean them into reliable tables, support batch and streaming, and allow analysts/ML teams to query the same trusted data.
- What would go wrong without it: Teams copy data into many systems, schema changes break pipelines, and historical corrections become painful.

## 9. System Design Angle

Clarify these requirements:

- data volume per day
- batch vs streaming ingestion
- update/delete/upsert needs
- query engines that must read the table
- freshness SLA
- retention and audit needs
- PII/security/governance needs
- cost constraints

Common design:

```text
OLTP DB -> CDC -> Kafka -> Spark/Flink -> Iceberg/Delta/Hudi tables on S3
                                      -> Trino/Spark SQL/BI
                                      -> ML training and feature pipelines
```

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| open, cheap storage | more moving parts |
| ACID-like table behavior | metadata/catalog operations |
| batch and streaming support | table maintenance jobs |
| time travel and rollback | storage for old snapshots |
| multiple engines | compatibility testing |

## 11. Failure Modes

- Failure: Writer fails halfway.
- Symptom: data files may exist but table snapshot is not committed.
- Recovery: uncommitted files can be cleaned.
- Prevention: atomic metadata commits.

- Failure: Too many small files.
- Symptom: slow query planning and scans.
- Recovery: compaction.
- Prevention: tuned writer file sizes and scheduled optimization.

- Failure: Catalog unavailable.
- Symptom: engines cannot find table metadata.
- Recovery: catalog restore/failover.
- Prevention: managed, backed-up catalog.

## 12. Common Mistakes

- Mistake: Thinking Parquet alone is a lakehouse.
- Why it is wrong: Parquet is a file format, not a transaction/table management layer.
- Better approach: Use a table format like Iceberg, Delta Lake, or Hudi.

- Mistake: Ignoring maintenance.
- Why it is wrong: tables accumulate small files, old metadata, and poor layout.
- Better approach: schedule compaction, cleanup, clustering, and statistics refresh.

## 13. Mini Example

```text
orders table =
  data files: orders_001.parquet, orders_002.parquet
  metadata: schema, partition rules, current snapshot, old snapshots
  catalog: "orders" points to latest metadata file
```

## 14. Interview Questions

1. What is a data lakehouse?
2. How is a lakehouse different from a data lake?
3. Why do table formats matter?
4. Where do Spark, Trino, and object storage fit?
5. What maintenance jobs do lakehouse tables need?

## 15. Interview Speak

"A lakehouse stores open data files in object storage but adds table-format metadata for ACID commits, schema management, snapshots, time travel, and efficient querying. I would use it when I need cheap scalable storage plus reliable analytics for Spark, Trino, Flink, BI, and ML workloads."

## 16. Quick Recall

- One-line summary: A lakehouse is a managed table layer on top of data lake storage.
- Three keywords: object storage, table format, catalog.
- One trap: Confusing Parquet files with a full lakehouse table.
- One memory trick: Lakehouse = lake storage plus warehouse rules.
