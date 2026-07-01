# Phase 6 Review: Modern Data Lakehouse

## 1. Phase Summary

Phase 6 explains how modern data lakehouse systems make data lakes reliable enough for serious analytics.

The core idea:

```text
object storage gives cheap scalable files
table formats give reliable table behavior
query engines process and serve the data
maintenance keeps the tables healthy
```

If you remember only one sentence:

```text
A lakehouse is not just Parquet files; it is Parquet/ORC/Avro files plus table metadata, snapshots, commits, catalogs, and maintenance.
```

## 2. Mental Model

```text
Sources
  -> ingestion jobs
  -> object storage
  -> table format metadata
  -> catalog
  -> Spark/Flink/Trino/BI/ML
```

The table format answers:

- Which files belong to the table right now?
- What schema is valid?
- What snapshot is current?
- Which older snapshots can be queried?
- What files were added or removed?
- How are partitions defined?
- Which files can be skipped?

## 3. Must-Know Concepts

| Concept | Beginner Meaning | Interview Meaning |
|---|---|---|
| lakehouse | data lake with warehouse-like table reliability | open storage plus ACID/table metadata |
| table format | makes files behave like a table | metadata, snapshots, commits, schema, deletes |
| catalog | table name lookup service | maps table names to metadata locations |
| snapshot | table version | consistent set of files at a point in time |
| time travel | query older table version | useful for rollback, audit, debugging |
| ACID | reliable changes | atomic metadata commits over files |
| compaction | combine small files | improves planning and scans |
| upsert | update or insert by key | implemented with MERGE/rewrite/delete files |
| partition evolution | change partition layout over time | new specs without full historical rewrite |
| hidden partitioning | users query normal columns | metadata handles partition transforms |
| clustering | colocate similar data | improves data skipping |
| vacuum | remove old files safely | retention vs recovery trade-off |

## 4. Tool Comparison

| Tool | Best Mental Model | Strong Fit | Watch Out |
|---|---|---|---|
| Apache Iceberg | scalable table metadata and snapshots | multi-engine lakehouse, partition evolution, hidden partitioning | catalog and engine compatibility |
| Delta Lake | Parquet plus transaction log | Spark/Databricks lakehouse, MERGE, OPTIMIZE, time travel | retention, VACUUM, feature support outside main platform |
| Apache Hudi | upsert-focused lake tables | CDC, mutable datasets, incremental processing | key design, indexing, compaction |

Quick memory:

```text
Iceberg -> open scalable metadata model
Delta   -> transaction log and strong Spark/Databricks workflow
Hudi    -> CDC/upsert-heavy workloads
```

## 5. File Format Vs Table Format

| Question | File Format | Table Format |
|---|---|---|
| Example | Parquet, ORC, Avro | Iceberg, Delta, Hudi |
| Scope | one file | whole table |
| Stores records? | yes | no, it tracks files/metadata |
| Transactions? | no | yes, through commit metadata/log |
| Time travel? | no | yes, if old metadata/files retained |
| Schema evolution? | limited/file-level | table-level management |

Strong interview line:

> Parquet makes each file efficient. Iceberg, Delta, or Hudi make many files behave like one reliable table.

## 6. How Lakehouse Writes Work

```text
1. Writer reads current table metadata.
2. Writer creates new data files.
3. Writer creates metadata/log changes.
4. Writer commits atomically.
5. New snapshot/version becomes current.
6. Readers only see committed snapshots.
```

If the writer fails before commit:

```text
data files may exist in storage
but they are not part of the official table
cleanup can remove them later
```

## 7. Snapshot Isolation

Snapshot isolation means:

```text
Each reader sees one stable version of the table.
```

Example:

```text
Query A starts on Snapshot 10.
Writer commits Snapshot 11.
Query A still reads Snapshot 10.
Query B starts later and reads Snapshot 11.
```

Why it matters:

- avoids partial reads
- supports concurrent reads and writes
- makes long queries consistent
- enables time travel and rollback

## 8. Time Travel

Time travel lets you query:

- a previous version
- a previous timestamp
- a previous commit/snapshot

Use cases:

- debug bad pipeline writes
- recover deleted data
- compare before/after states
- reproduce ML training data
- audit past reports

Big warning:

```text
Time travel works only while old files and metadata still exist.
Cleanup shortens the time travel window.
```

## 9. ACID On Data Lake

ACID mapping:

| ACID Letter | Lakehouse Meaning |
|---|---|
| Atomicity | commit appears fully or not at all |
| Consistency | schema/table rules stay valid |
| Isolation | readers see stable snapshots |
| Durability | committed metadata/files persist |

Important explanation:

```text
Object storage stores files.
The table format provides table-level transaction behavior.
```

## 10. COW Vs MOR

| Strategy | What Happens | Best For | Cost |
|---|---|---|---|
| Copy-on-write | rewrite affected base files during update | read-heavy analytics | high write amplification |
| Merge-on-read | write changes separately and merge later | frequent updates/CDC | read amplification and compaction |

Fast memory:

```text
COW pays during write.
MOR pays during read until compaction.
```

## 11. Upserts

Upsert means:

```text
matched key -> update
missing key -> insert
```

Common pattern:

```text
OLTP database
  -> CDC stream
  -> Kafka
  -> Spark/Flink
  -> MERGE into lakehouse table
```

Things to clarify in design:

- What is the key?
- Are events ordered?
- Can updates arrive late?
- Are deletes/tombstones needed?
- Is history needed or only current state?
- What is the update rate?

## 12. Metadata Scaling

Large lakehouse tables need scalable metadata because they may contain:

- millions of files
- many partitions
- many snapshots
- many delete files
- many schema changes

Performance can be slow before data scanning starts.

Check:

- planning time
- file count
- average file size
- manifest/log size
- snapshot count
- partition count
- stats availability

## 13. Partitioning Concepts

### Partition Evolution

Partition evolution lets new data use a new partition strategy while old data keeps its old layout.

Example:

```text
old files: month(order_ts)
new files: day(order_ts)
metadata knows both
```

### Hidden Partitioning

Hidden partitioning lets users write:

```sql
WHERE event_ts >= '2026-07-01'
```

while the table internally prunes:

```text
days(event_ts)
```

This avoids exposing physical folder layout to users.

## 14. Clustering And Z-Ordering

Partitioning:

```text
broad data grouping
```

Clustering/Z-ordering:

```text
better row/file locality inside broad groups
```

Use clustering when:

- queries repeatedly filter by certain columns
- partitioning alone is not selective enough
- file-level stats/data skipping are supported
- maintenance cost is justified

Avoid:

- clustering too many columns
- clustering columns nobody filters
- reclustering too often without measuring benefit

## 15. Cleanup And Retention

Cleanup removes:

- old data files
- expired snapshots
- orphan files
- old logs/manifests

But cleanup can break:

- time travel
- rollback
- active long-running readers
- audit recovery

Choose retention using:

- max query duration
- rollback SLA
- audit/legal needs
- privacy requirements
- storage cost

## 16. Performance Tuning Checklist

When a lakehouse query is slow, ask:

1. Is planning slow or execution slow?
2. Are there too many small files?
3. Are partitions useful for query filters?
4. Are users missing date/time filters?
5. Are file stats available?
6. Would clustering help common filters?
7. Are delete/log files accumulating?
8. Are old snapshots/manifests bloating metadata?
9. Is the query scanning unnecessary columns?
10. Should this be a gold aggregate table?

## 17. Common Interview Questions

1. What is a data lakehouse?
2. How is a lakehouse different from a data lake?
3. What is a table format?
4. Difference between Parquet and Iceberg/Delta/Hudi?
5. Compare Iceberg, Delta, and Hudi.
6. How does snapshot isolation work?
7. How does time travel work?
8. What does ACID mean on a data lake?
9. How do lakehouse upserts work?
10. Copy-on-write vs merge-on-read?
11. What is compaction?
12. Why do small files hurt lakehouse performance?
13. What is hidden partitioning?
14. What is partition evolution?
15. How do you tune a slow lakehouse table?

## 18. Strong System Design Answer

Question:

> Design a lakehouse platform for an e-commerce company that needs analytics on orders, clicks, inventory, and customer profile updates.

Strong answer:

"I would use object storage like S3/ADLS/GCS as the durable data layer and store tables using an open lakehouse format such as Iceberg, Delta, or Hudi. Raw events and CDC records would land in bronze append-only tables. Spark or Flink jobs would clean, deduplicate, and merge data into silver tables. Gold tables would store business aggregates for dashboards.

For correctness, writes would go through the table format so commits are atomic and readers get snapshot isolation. For customer/profile CDC, I would use MERGE/upserts with stable keys and event versions. I would design partitions around common bounded filters like event date, use clustering or Z-ordering for frequent secondary filters, compact small files, expire old snapshots safely, and monitor planning time, scan time, file count, lag, and table freshness.

The main trade-offs are storage cost for time travel, compute cost for compaction/clustering, write amplification for updates, and engine compatibility across Spark, Flink, Trino, and BI tools."

## 19. Hands-On Project

Build a mini lakehouse simulation locally:

1. Create a small raw orders CSV.
2. Convert it into a "table" represented by data files and metadata JSON.
3. Add a new snapshot when new orders arrive.
4. Simulate a reader pinned to an old snapshot.
5. Add an upsert step by `order_id`.
6. Add a compaction step that merges small files.
7. Add cleanup that removes files not referenced by retained snapshots.

What this teaches:

- files vs table metadata
- snapshot isolation
- upsert logic
- compaction
- cleanup risk

## 20. Production Checklist

For every production lakehouse table, define:

- owner/team
- data contract/schema
- table format
- catalog
- partition strategy
- clustering/sort strategy
- expected file size
- compaction schedule
- cleanup retention
- time travel window
- upsert/delete rules
- PII policy
- freshness SLA
- quality checks
- monitoring alerts
- backfill/replay process

## 21. Quick Revision Cards

| Prompt | Answer |
|---|---|
| Lakehouse? | data lake storage plus table reliability |
| Table format? | metadata layer that manages table files/versions |
| Iceberg? | open scalable table format with snapshots/manifests |
| Delta? | Parquet plus `_delta_log` transaction history |
| Hudi? | upsert/CDC-focused lakehouse table format |
| Snapshot isolation? | each query reads one stable version |
| Time travel? | query older table versions |
| Compaction? | rewrite small files into bigger files |
| COW? | rewrite files on update |
| MOR? | write deltas, merge later |
| Vacuum? | delete old unreferenced files safely |
| Hidden partitioning? | users query normal columns, metadata prunes partitions |
| Tuning? | improve files, metadata, pruning, clustering, and queries |
