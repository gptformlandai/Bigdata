# Phase 3: Hadoop Ecosystem

Phase 3 is the first real Big Data tool phase.

Hadoop matters because it introduced the classic pattern behind many modern data platforms:

```text
store huge files across many cheap machines
process data close to where it lives
recover from machine failure automatically
```

Even when modern teams use Spark, Databricks, S3, BigQuery, Snowflake, or lakehouse tools, Hadoop concepts still show up everywhere: distributed storage, blocks, metadata, replication, batch jobs, cluster resources, Hive tables, partitions, and file formats.

## Topics

| # | Topic | Status |
|---:|---|---|
| 061 | Hadoop overview | Complete |
| 062 | HDFS | Complete |
| 063 | NameNode and DataNode | Complete |
| 064 | HDFS block storage | Complete |
| 065 | Replication factor | Complete |
| 066 | MapReduce | Complete |
| 067 | YARN | Complete |
| 068 | Hive | Complete |
| 069 | Hive metastore | Complete |
| 070 | Partitioning in Hive | Complete |
| 071 | Bucketing in Hive | Complete |
| 072 | HBase | Complete |
| 073 | Sqoop | Complete |
| 074 | Flume | Complete |
| 075 | Oozie | Complete |
| 076 | Hadoop limitations | Complete |
| 077 | Why Spark replaced MapReduce for many workloads | Complete |

## Phase Goal

By the end of this phase, you should be able to explain:

- what Hadoop is and why it was created
- how HDFS stores massive files across machines
- what NameNode and DataNode do
- why blocks and replication matter
- how MapReduce processes data in batch
- how YARN manages cluster resources
- why Hive made Hadoop usable through SQL
- how Hive metastore, partitions, and buckets work
- what HBase, Sqoop, Flume, and Oozie were used for
- why Hadoop was important but Spark and cloud-native platforms became more common

## Suggested Study Flow

1. Read Topics 061-065 to understand Hadoop storage.
2. Read Topics 066-067 to understand Hadoop compute and resource management.
3. Read Topics 068-071 to understand SQL-on-Hadoop through Hive.
4. Read Topics 072-075 to understand the broader Hadoop ecosystem.
5. Read Topics 076-077 to understand Hadoop's limitations and why newer tools evolved.
6. Finish with `phase-03-review.md`.
