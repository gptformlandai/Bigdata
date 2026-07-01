# Topic 068: Hive

## 1. Goal

Understand Hive as the SQL layer that made Hadoop usable for analysts and data engineers.

## 2. Baby Intuition

HDFS stores files, but most people do not want to write Java MapReduce jobs just to answer questions.

Hive says:

```text
Write SQL.
I will translate it into distributed processing over files.
```

It made Hadoop feel more like a data warehouse.

## 3. What It Is

- Simple definition: Hive lets you query data in Hadoop using SQL-like syntax.
- Technical definition: Apache Hive is a data warehouse layer on Hadoop that stores table metadata in the Hive metastore and executes SQL queries over files in HDFS or compatible storage.
- Category: SQL-on-Hadoop / data warehouse layer.
- Related terms: HiveQL, metastore, table, partition, bucketing, SerDe, external table.

## 4. Why It Exists

MapReduce was powerful but hard:

- lots of Java code
- slow development
- not friendly for analysts
- repetitive logic for joins and aggregations

Hive exists because teams needed SQL access to huge files in Hadoop.

Without Hive:

```text
simple business question -> custom MapReduce job
```

With Hive:

```text
simple business question -> SQL query
```

## 5. Where It Fits In A Data Platform

```text
Sources -> HDFS files -> Hive tables/metastore -> SQL queries -> reports/ETL outputs
```

Hive sits above storage.

It can use engines such as:

- MapReduce
- Tez
- Spark in some setups

Hive stores metadata, not usually the actual bytes. Actual table data lives in files.

## 6. How It Works Step By Step

When you run a Hive query:

1. You submit HiveQL.
2. Hive parses the SQL.
3. Hive checks table metadata in metastore.
4. Hive plans a distributed job.
5. Execution engine reads files from HDFS.
6. Data is filtered, joined, grouped, or transformed.
7. Results are returned or written as files.

Example:

```sql
SELECT customer_id, SUM(amount) AS revenue
FROM orders
WHERE dt = '2026-07-01'
GROUP BY customer_id;
```

Hive uses metadata to find where `orders` data is stored and which partition maps to `dt = '2026-07-01'`.

## 7. How To Use It Practically

Create a table:

```sql
CREATE TABLE orders (
    order_id STRING,
    customer_id STRING,
    amount DOUBLE,
    status STRING
)
PARTITIONED BY (dt STRING)
STORED AS PARQUET;
```

Query:

```sql
SELECT status, COUNT(*) AS order_count
FROM orders
WHERE dt = '2026-07-01'
GROUP BY status;
```

Common table types:

- managed table: Hive manages data location/lifecycle
- external table: Hive tracks metadata for data stored externally

Production pattern:

```text
Use external tables for data lake files.
Use Parquet/ORC for analytics.
Partition by date when queries filter by date.
```

## 8. Real-World Scenario

- Product/system: Marketing analytics warehouse on Hadoop.
- Problem: Analysts need campaign performance metrics from TBs of click logs.
- How Hive helps: Analysts write SQL instead of MapReduce code.
- What would go wrong without it: Every question would require engineering-heavy batch jobs.

## 9. System Design Angle

Hive is useful when:

- data is large
- SQL access is needed
- latency can be seconds to minutes
- data lives as files
- batch analytics is acceptable

Hive is not ideal for:

- high-QPS application serving
- row-level transactions in classic setups
- sub-second dashboards unless optimized with other engines

Design considerations:

- file format
- partitioning
- metastore reliability
- query engine
- data layout
- small files

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| SQL on huge files | slower than OLTP DBs |
| easier analytics | depends on file layout |
| table abstraction over HDFS | metastore dependency |
| integrates with Hadoop ecosystem | tuning needed for performance |

## 11. Failure Modes

- Failure: Metastore unavailable.
- Symptom: queries cannot find table metadata.
- Recovery: restore metastore service/database.
- Prevention: HA metastore and database backups.

- Failure: Bad partition layout.
- Symptom: queries scan too much data.
- Recovery: repartition/rewrite table.
- Prevention: choose partition keys from access patterns.

- Failure: Too many small files.
- Symptom: slow queries and planning overhead.
- Recovery: compact files.
- Prevention: batch writes and optimize file sizes.

## 12. Common Mistakes

- Mistake: Thinking Hive stores data like MySQL.
- Why it is wrong: Hive tables usually point to files in HDFS/object storage.
- Better approach: Think table metadata + files.

- Mistake: Querying without partition filters.
- Why it is wrong: Hive may scan massive data.
- Better approach: filter by partition columns when possible.

- Mistake: Using text/CSV forever.
- Why it is wrong: analytics scan cost is high.
- Better approach: use Parquet or ORC.

## 13. Mini Example

External table over existing files:

```sql
CREATE EXTERNAL TABLE raw_clicks (
    user_id STRING,
    page STRING,
    event_time STRING
)
PARTITIONED BY (dt STRING)
STORED AS PARQUET
LOCATION '/data/raw/clicks';
```

Hive now knows how to query files under `/data/raw/clicks`.

## 14. Interview Questions

1. What problem does Hive solve?
2. Is Hive a database?
3. What is the difference between managed and external tables?
4. Why does Hive need a metastore?
5. How do partitioning and file format affect Hive performance?

## 15. Interview Speak

"Hive is a SQL-on-Hadoop layer. It lets users query large files in HDFS using HiveQL while storing table definitions, schema, and partition metadata in the metastore. It is good for batch analytics over large datasets, but performance depends heavily on file format, partitioning, and execution engine."

## 16. Quick Recall

- One-line summary: Hive gives SQL table abstraction over Hadoop files.
- Three keywords: HiveQL, metastore, partitions.
- One trap: Treating Hive like an OLTP database.
- One memory trick: HDFS has files; Hive gives them table names.
