# Topic 069: Hive Metastore

## 1. Goal

Understand Hive metastore as the metadata brain behind Hive tables.

## 2. Baby Intuition

If HDFS is a warehouse full of boxes, the Hive metastore is the catalog that says:

- what each table is called
- which columns it has
- where its files live
- which partitions exist

Without the catalog, you just have files.

## 3. What It Is

- Simple definition: Hive metastore stores table metadata.
- Technical definition: The Hive metastore is a service and backing database that stores metadata about databases, tables, columns, partitions, storage locations, SerDes, and file formats.
- Category: Metadata service/catalog.
- Related terms: catalog, schema, partition metadata, external table, SerDe, table location.

## 4. Why It Exists

Files alone do not tell enough.

Example file path:

```text
/data/orders/dt=2026-07-01/part-0000.parquet
```

Important questions:

- What is the table name?
- What columns exist?
- What are the data types?
- What format is the file?
- Which partition does it belong to?
- Where is the table root location?

The metastore answers these questions.

## 5. Where It Fits In A Data Platform

```text
Query engine -> Hive Metastore -> table/partition metadata -> files in HDFS
```

Used by:

- Hive
- Spark SQL
- Presto/Trino
- Impala
- some lakehouse integrations

The metastore is a shared catalog.

## 6. How It Works Step By Step

When creating a table:

1. User runs `CREATE TABLE`.
2. Hive records table metadata in metastore.
3. Metadata includes schema, location, format, partitions.
4. Actual data files live in HDFS or storage path.

When querying:

1. Query engine receives SQL.
2. It asks metastore for table metadata.
3. It gets schema and file locations.
4. It plans file scans.
5. It reads actual data files.

## 7. How To Use It Practically

Show table metadata:

```sql
DESCRIBE orders;
DESCRIBE FORMATTED orders;
SHOW PARTITIONS orders;
SHOW CREATE TABLE orders;
```

Repair partition metadata when files exist but metastore does not know them:

```sql
MSCK REPAIR TABLE orders;
```

Common production issue:

```text
Files exist in storage, but query returns no data because partitions are not registered.
```

## 8. Real-World Scenario

- Product/system: Shared analytics lake.
- Problem: Many engines need to query the same tables.
- How metastore helps: Provides shared table schema and location metadata.
- What would go wrong without it: Each tool/team would define tables differently and queries would become inconsistent.

## 9. System Design Angle

The metastore is often a critical dependency.

If it is down:

- queries may fail before reading data
- jobs may not find partitions
- table creation/alteration fails

Design considerations:

- high availability
- backing database reliability
- schema migration safety
- partition count scaling
- access controls
- catalog consistency

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| shared table metadata | central dependency |
| SQL abstraction over files | metadata scaling limits |
| partition pruning | partition registration overhead |
| multi-engine interoperability | compatibility issues |

## 11. Failure Modes

- Failure: Metastore service down.
- Symptom: query engines cannot fetch metadata.
- Recovery: restart/failover service.
- Prevention: HA metastore.

- Failure: Backing database corrupted/unavailable.
- Symptom: metadata lost or inaccessible.
- Recovery: restore database backup.
- Prevention: backups, replication, monitoring.

- Failure: Too many partitions.
- Symptom: slow planning or metastore pressure.
- Recovery: partition pruning, compaction, redesign partition strategy.
- Prevention: avoid overly granular partitions.

## 12. Common Mistakes

- Mistake: Thinking metastore stores table data.
- Why it is wrong: it stores metadata; files store data.
- Better approach: table metadata vs table bytes.

- Mistake: Adding partitions in storage but not metastore.
- Why it is wrong: query engines may not discover them.
- Better approach: register partitions or use repair/discovery mechanisms.

## 13. Mini Example

Metastore record roughly says:

```text
table: orders
columns: order_id string, amount double
format: parquet
location: /warehouse/orders
partitions: dt=2026-07-01, dt=2026-07-02
```

## 14. Interview Questions

1. What does Hive metastore store?
2. Does metastore store actual data?
3. Why do query engines need metastore?
4. What happens if partition metadata is missing?
5. Why can too many partitions hurt metastore?

## 15. Interview Speak

"Hive metastore is the metadata catalog for Hive tables. It stores schema, table locations, partitions, file formats, and SerDe information, while actual data lives in HDFS or object storage. Many engines rely on it, so availability and metadata scaling are important."

## 16. Quick Recall

- One-line summary: Hive metastore is the catalog that maps table names to file metadata.
- Three keywords: schema, location, partitions.
- One trap: Saying metastore stores the actual data.
- One memory trick: Metastore is the address book for tables.
