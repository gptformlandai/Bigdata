# Topic 073: Sqoop

## 1. Goal

Understand Sqoop as a Hadoop-era tool for bulk moving data between relational databases and Hadoop.

## 2. Baby Intuition

Companies had lots of data in relational databases like MySQL, Oracle, and SQL Server.

Hadoop needed that data for analytics.

Sqoop acted like a bulk data truck:

```text
database tables <-> Hadoop files
```

## 3. What It Is

- Simple definition: Sqoop imports/export data between relational databases and Hadoop.
- Technical definition: Apache Sqoop is a command-line tool that transfers bulk data between structured datastores such as relational databases and Hadoop storage like HDFS, Hive, or HBase.
- Category: Batch data ingestion/export tool.
- Related terms: JDBC, import, export, split-by, mapper, full load, incremental load.

## 4. Why It Exists

Hadoop needed data from existing databases.

Before Sqoop, teams had to write custom scripts to:

- connect to databases
- split queries
- export rows
- convert to files
- load into HDFS/Hive
- handle large tables

Sqoop automated parallel bulk transfer.

## 5. Where It Fits In A Data Platform

```text
Relational DB -> Sqoop -> HDFS/Hive
HDFS/Hive -> Sqoop -> Relational DB
```

Common use:

- nightly database table import to Hadoop
- export aggregates from Hadoop to reporting database
- migrate structured tables into data lake

## 6. How It Works Step By Step

Import flow:

1. Sqoop connects to database using JDBC.
2. It reads table metadata.
3. It chooses a split column.
4. It launches parallel map tasks.
5. Each mapper imports a range of rows.
6. Rows are written to HDFS or Hive.

Example:

```text
orders table id 1-1000000
mapper 1 imports 1-250000
mapper 2 imports 250001-500000
mapper 3 imports 500001-750000
mapper 4 imports 750001-1000000
```

## 7. How To Use It Practically

Example import:

```bash
sqoop import \
  --connect jdbc:mysql://db.example.com/sales \
  --username user \
  --table orders \
  --target-dir /data/raw/orders \
  --split-by order_id \
  --num-mappers 4
```

Hive import idea:

```bash
sqoop import \
  --connect jdbc:mysql://db.example.com/sales \
  --username user \
  --table orders \
  --hive-import \
  --hive-table raw_orders
```

Practical warning:

```text
Do not overload the source database.
```

## 8. Real-World Scenario

- Product/system: Nightly enterprise reporting.
- Problem: Operational order data lives in Oracle, but analytics runs on Hadoop.
- How Sqoop helps: Imports order tables into HDFS/Hive every night.
- What would go wrong without it: Teams would build fragile custom scripts and slow single-threaded exports.

## 9. System Design Angle

Sqoop is a batch ingestion tool.

Good for:

- bulk table loads
- nightly imports
- simple full/incremental loads

Not ideal for:

- real-time CDC
- low-latency replication
- complex transformations
- very sensitive production DBs without throttling

Modern alternatives:

- Debezium for CDC
- Kafka Connect JDBC
- cloud database migration services
- managed ELT tools

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| simple DB-to-Hadoop transfer | batch latency |
| parallel imports | source DB load |
| easy Hive integration | limited CDC capability |
| avoids custom scripts | operational tuning |

## 11. Failure Modes

- Failure: Source DB overloaded.
- Symptom: production database slows.
- Recovery: reduce mappers, throttle, use replica.
- Prevention: import from read replica and schedule off-peak.

- Failure: Bad split column.
- Symptom: skewed import where one mapper runs forever.
- Recovery: choose better split key.
- Prevention: use numeric evenly distributed column.

- Failure: Partial import.
- Symptom: incomplete HDFS data.
- Recovery: rerun into temp path and atomic rename.
- Prevention: validate row counts.

## 12. Common Mistakes

- Mistake: Using too many mappers.
- Why it is wrong: can overload the database.
- Better approach: tune mapper count and use read replicas.

- Mistake: No row count validation.
- Why it is wrong: imports may silently miss data.
- Better approach: compare source and target counts/checksums.

## 13. Mini Example

Incremental import idea:

```bash
sqoop import \
  --table orders \
  --check-column updated_at \
  --incremental lastmodified \
  --last-value '2026-07-01 00:00:00'
```

This imports rows updated after the last value.

## 14. Interview Questions

1. What problem does Sqoop solve?
2. How does Sqoop parallelize imports?
3. What is `split-by`?
4. How can Sqoop hurt a production database?
5. What modern tools replace Sqoop for CDC?

## 15. Interview Speak

"Sqoop is a Hadoop-era bulk transfer tool for moving data between relational databases and Hadoop. It uses JDBC and parallel map tasks to import table ranges into HDFS or Hive. It is useful for batch loads, but must be tuned carefully to avoid overloading source databases, and modern CDC tools are better for real-time replication."

## 16. Quick Recall

- One-line summary: Sqoop bulk-moves relational tables into or out of Hadoop.
- Three keywords: JDBC, import, split-by.
- One trap: Using Sqoop as real-time CDC.
- One memory trick: Sqoop is a batch moving truck for database tables.
