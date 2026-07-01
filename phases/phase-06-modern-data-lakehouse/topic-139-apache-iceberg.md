# Topic 139: Apache Iceberg

## 1. Goal

Understand Apache Iceberg as an open table format for large analytical datasets.

## 2. Baby Intuition

Iceberg is like a smart table notebook.

Instead of asking every engine to guess which files belong to a table, Iceberg keeps a precise list of files, snapshots, schema changes, and partition rules.

## 3. What It Is

- Simple definition: Apache Iceberg is an open table format for data lakehouse tables.
- Technical definition: Iceberg manages large analytic tables using metadata files, manifests, snapshots, schemas, partition specs, and atomic commits over data files stored in systems like S3, GCS, ADLS, or HDFS.
- Category: Open lakehouse table format.
- Related terms: snapshot, manifest, metadata file, partition evolution, hidden partitioning, Spark, Flink, Trino.

## 4. Why It Exists

Older Hive-style tables had issues:

- partitions were exposed as physical folders
- changing partition layout was hard
- large table metadata could become slow
- readers could see inconsistent file lists
- deletes/upserts were difficult

Iceberg was created to make huge data lake tables safer, more scalable, and more engine-independent.

## 5. Where It Fits In A Data Platform

```text
Object storage holds Parquet/ORC/Avro files
  -> Iceberg metadata tracks table state
  -> catalog points engines to latest metadata
  -> Spark/Flink/Trino query and write safely
```

Iceberg is not a compute engine. It is the table layer.

## 6. How It Works Step By Step

1. A table has a metadata file.
2. Metadata points to snapshots.
3. Snapshots point to manifest lists.
4. Manifest lists point to manifests.
5. Manifests list data files and file-level statistics.
6. A writer creates new data files and metadata.
7. The writer commits by atomically updating the catalog pointer to a new metadata file.
8. Readers use a snapshot, so they see a consistent table version.

Tiny mental model:

```text
catalog -> metadata -> snapshot -> manifests -> data files
```

## 7. How To Use It Practically

Example actions:

```sql
CREATE TABLE lake.orders (
  order_id BIGINT,
  customer_id BIGINT,
  order_ts TIMESTAMP,
  amount DECIMAL(10,2)
) USING iceberg
PARTITIONED BY (days(order_ts));
```

Common use cases:

- large fact tables
- slowly changing analytical tables
- CDC ingestion into lake
- multi-engine access with Spark, Flink, and Trino
- tables that need partition evolution

## 8. Real-World Scenario

- Product/system: Enterprise order lakehouse.
- Problem: The table grows by billions of rows and query teams use both Spark and Trino.
- How Iceberg helps: It gives both engines a consistent snapshot, scalable metadata, hidden partitioning, and safe table evolution.
- What would go wrong without it: Teams may manually manage folders and accidentally query partial or stale data.

## 9. System Design Angle

Use Iceberg when:

- many engines must read the same table
- partition layout may evolve
- huge table metadata must scale
- snapshot isolation and time travel are needed
- object storage is the main storage layer

Avoid assuming every engine supports every Iceberg feature equally. In production, always test the exact engine versions and catalog integration.

## 10. Trade-offs

| Pros | Cons |
|---|---|
| open table format | requires catalog setup |
| strong metadata model | maintenance still needed |
| hidden partitioning | learning curve for table operations |
| partition evolution | engine compatibility must be checked |
| snapshot isolation | old snapshots consume storage |

## 11. Failure Modes

- Failure: Commit conflict.
- Symptom: writer cannot commit because another writer updated the table first.
- Recovery: retry with latest metadata.
- Prevention: use supported writers and controlled concurrency.

- Failure: Metadata grows too large.
- Symptom: slow planning.
- Recovery: expire snapshots and rewrite manifests.
- Prevention: table maintenance.

- Failure: Orphan files.
- Symptom: data files exist but are not referenced.
- Recovery: remove orphan files carefully.
- Prevention: clean failed writes after retention window.

## 12. Common Mistakes

- Mistake: Manually deleting data files.
- Why it is wrong: Iceberg metadata may still reference them.
- Better approach: use Iceberg delete/expire operations.

- Mistake: Treating partitions as folder contracts.
- Why it is wrong: Iceberg can hide and evolve partitioning.
- Better approach: query logical columns and let Iceberg prune files.

## 13. Mini Example

```text
Snapshot 10 -> files A, B, C
Writer adds file D
Snapshot 11 -> files A, B, C, D
Readers on Snapshot 10 keep seeing A, B, C until they refresh.
```

## 14. Interview Questions

1. What is Apache Iceberg?
2. How does Iceberg manage table metadata?
3. What is hidden partitioning?
4. How does Iceberg support snapshot isolation?
5. Why choose Iceberg over Hive-style tables?

## 15. Interview Speak

"Iceberg is an open table format for large lakehouse tables. It stores table state in metadata, snapshots, and manifests, while data stays in open files like Parquet. It is useful for multi-engine analytics, snapshot isolation, partition evolution, hidden partitioning, and scalable metadata management."

## 16. Quick Recall

- One-line summary: Iceberg is a scalable metadata and snapshot layer for open lakehouse tables.
- Three keywords: snapshots, manifests, hidden partitions.
- One trap: Thinking Iceberg is a database engine.
- One memory trick: Iceberg is the table map, not the warehouse worker.
