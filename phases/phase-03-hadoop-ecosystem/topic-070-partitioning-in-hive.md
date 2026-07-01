# Topic 070: Partitioning In Hive

## 1. Goal

Understand Hive partitioning as a way to organize table files so queries scan less data.

## 2. Baby Intuition

Imagine a library with books sorted by year.

If you need books from 2026, you go straight to the 2026 shelf instead of searching every shelf.

Hive partitioning does this for data.

## 3. What It Is

- Simple definition: Hive partitioning stores table data in separate folders based on partition column values.
- Technical definition: Hive partitions divide table data by one or more partition columns, mapping each partition value to a directory and metadata entry.
- Category: Data layout optimization.
- Related terms: partition column, partition pruning, directory layout, dynamic partitioning, metastore partition.

## 4. Why It Exists

Big tables are expensive to scan.

Without partitioning:

```text
query one day -> scan all days
```

With partitioning:

```text
query one day -> scan only that day folder
```

Hive partitioning exists to reduce scan cost and improve query speed.

## 5. Where It Fits In A Data Platform

```text
HDFS table files -> partition folders -> Hive metastore -> SQL partition pruning
```

Common partition columns:

- date: `dt`
- hour: `hour`
- region
- country
- source
- tenant, carefully

Most common beginner pattern:

```text
partition by date
```

## 6. How It Works Step By Step

Table definition:

```sql
CREATE TABLE clicks (
    user_id STRING,
    page STRING
)
PARTITIONED BY (dt STRING)
STORED AS PARQUET;
```

HDFS layout:

```text
/warehouse/clicks/dt=2026-07-01/
/warehouse/clicks/dt=2026-07-02/
```

Query:

```sql
SELECT COUNT(*)
FROM clicks
WHERE dt = '2026-07-01';
```

Hive sees the partition filter and scans only:

```text
/warehouse/clicks/dt=2026-07-01/
```

This is called partition pruning.

## 7. How To Use It Practically

Add a partition:

```sql
ALTER TABLE clicks
ADD PARTITION (dt='2026-07-01')
LOCATION '/warehouse/clicks/dt=2026-07-01';
```

Show partitions:

```sql
SHOW PARTITIONS clicks;
```

Dynamic partition insert:

```sql
INSERT OVERWRITE TABLE clicks_by_day PARTITION (dt)
SELECT user_id, page, dt
FROM raw_clicks;
```

Production habit:

```text
Always include partition filters when querying large partitioned tables.
```

## 8. Real-World Scenario

- Product/system: Daily clickstream analytics.
- Problem: Analysts usually query one day or one week of data.
- How partitioning helps: Store files by `dt`, so queries skip unrelated dates.
- What would go wrong without it: Every query scans months or years of data.

## 9. System Design Angle

Partitioning affects:

- query cost
- query latency
- file layout
- metastore size
- ingestion complexity

Good partition key:

- used frequently in filters
- not too high cardinality
- creates partitions of reasonable size

Bad partition key:

- unique user id for massive user base
- timestamp down to second
- field rarely used in filters

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| less data scanned | more metadata |
| faster queries with filters | bad keys create tiny partitions |
| easier data retention by date | partition management overhead |
| cleaner file organization | skewed partitions possible |

## 11. Failure Modes

- Failure: Query missing partition filter.
- Symptom: full table scan and slow query.
- Recovery: add filter or optimize table.
- Prevention: query guardrails and education.

- Failure: Too many small partitions.
- Symptom: metastore and planning slowdown.
- Recovery: reduce partition granularity.
- Prevention: choose partition keys carefully.

- Failure: Partition files exist but metadata missing.
- Symptom: query misses data.
- Recovery: add partition or repair table.
- Prevention: ingestion registers partitions correctly.

## 12. Common Mistakes

- Mistake: Partitioning by high-cardinality user id.
- Why it is wrong: creates too many tiny partitions.
- Better approach: use date or business dimensions with manageable cardinality.

- Mistake: Thinking partition column must be inside file rows.
- Why it is wrong: in Hive, partition value is often encoded in folder path and metastore.
- Better approach: understand directory-based partitioning.

## 13. Mini Example

Bad:

```text
PARTITIONED BY (user_id)
```

Could create millions of folders.

Better:

```text
PARTITIONED BY (dt)
```

For time-filtered analytics.

## 14. Interview Questions

1. What is Hive partitioning?
2. What is partition pruning?
3. Why is date a common partition key?
4. Why is high-cardinality partitioning risky?
5. What happens if partition metadata is missing?

## 15. Interview Speak

"Hive partitioning organizes table data into directories by partition values, commonly date. It improves query performance through partition pruning, where the engine scans only matching partitions. The trade-off is metadata and file management, so partition keys should match common filters without creating too many tiny partitions."

## 16. Quick Recall

- One-line summary: Hive partitions let queries skip folders they do not need.
- Three keywords: dt, pruning, folders.
- One trap: Over-partitioning.
- One memory trick: Date shelf, not every-user shelf.
