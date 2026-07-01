# Phase 3 Review: Hadoop Ecosystem

This review checks whether you understand Hadoop from baby-level intuition to interview-ready system design reasoning.

## Phase Summary

Phase 3 covered the Hadoop ecosystem:

- Hadoop overview
- HDFS distributed storage
- NameNode and DataNode
- HDFS blocks and replication
- MapReduce batch processing
- YARN resource management
- Hive SQL-on-Hadoop
- Hive metastore, partitioning, and bucketing
- HBase, Sqoop, Flume, and Oozie
- Hadoop limitations
- why Spark replaced MapReduce for many workloads

Main idea:

```text
Hadoop made it possible to store and process huge datasets across many machines.
```

## Checkpoint 1: Topics 061-065

Topics:

- Hadoop overview
- HDFS
- NameNode and DataNode
- HDFS block storage
- Replication factor

### Quiz

1. What are the main components of Hadoop?
2. What does HDFS store?
3. What is the difference between NameNode and DataNode?
4. Why does HDFS split files into blocks?
5. Why is replication factor 3 common?

### Practical Exercise

Given:

```text
file size = 1 TB
block size = 128 MB
replication factor = 3
```

Calculate:

- number of logical blocks
- number of physical block replicas
- approximate physical storage

### Mini System Design Question

> You need to store 500 TB of daily logs for batch analytics. How would HDFS store this data and protect it from node failures?

Strong direction:

- Split files into large blocks.
- Store blocks across DataNodes.
- Replicate each block.
- NameNode tracks metadata.
- DataNodes store actual bytes.
- Re-replicate when nodes fail.

### Recap Table

| Concept | Must Remember |
|---|---|
| Hadoop | distributed storage + batch processing ecosystem |
| HDFS | distributed file system |
| NameNode | metadata and block locations |
| DataNode | actual block storage |
| Block | large file chunk |
| Replication factor | number of block copies |

## Checkpoint 2: Topics 066-067

Topics:

- MapReduce
- YARN

### Quiz

1. What does a mapper do?
2. What happens during shuffle?
3. What does a reducer do?
4. What problem does YARN solve?
5. What is a YARN container?

### Practical Exercise

Write the map and reduce logic for:

```text
Count number of orders per customer.
```

Think:

```text
mapper: customer_id -> 1
reducer: customer_id -> sum(counts)
```

### Mini System Design Question

> A Hadoop cluster is shared by three teams. One team runs huge jobs and blocks everyone else. What helps?

Strong direction:

- YARN queues.
- Capacity/fair scheduling.
- Resource limits.
- Monitoring.
- Priority or SLA-based queue design.

### Recap Table

| Concept | Must Remember |
|---|---|
| Map | process records into key-value pairs |
| Shuffle | group values by key |
| Reduce | aggregate grouped values |
| YARN | cluster resource manager |
| Container | CPU/memory allocation unit |

## Checkpoint 3: Topics 068-071

Topics:

- Hive
- Hive metastore
- Partitioning in Hive
- Bucketing in Hive

### Quiz

1. Why did Hive become popular?
2. What does the Hive metastore store?
3. Does Hive metastore store actual table data?
4. What is partition pruning?
5. How is bucketing different from partitioning?

### Practical Exercise

Design a Hive table for clickstream data:

- choose file format
- choose partition column
- choose whether bucketing is useful
- write a simple `CREATE TABLE`
- write a query that uses partition pruning

### Mini System Design Question

> Analysts frequently query only the last 7 days of clickstream data. How would you design the Hive table?

Strong direction:

- Store table as Parquet or ORC.
- Partition by date.
- Ensure queries filter by `dt`.
- Avoid too many tiny files.
- Keep metastore partitions manageable.

### Recap Table

| Concept | Must Remember |
|---|---|
| Hive | SQL over Hadoop files |
| Metastore | table metadata catalog |
| Partitioning | folders by column value |
| Partition pruning | skip unrelated folders |
| Bucketing | hash rows into fixed files |

## Checkpoint 4: Topics 072-077

Topics:

- HBase
- Sqoop
- Flume
- Oozie
- Hadoop limitations
- Why Spark replaced MapReduce

### Quiz

1. Why was HBase needed if HDFS already existed?
2. What problem does Sqoop solve?
3. What are Flume source, channel, and sink?
4. What does Oozie coordinate?
5. Why is Spark faster than MapReduce for many workloads?

### Practical Exercise

For each requirement, choose the Hadoop-era tool:

| Requirement | Tool |
|---|---|
| SQL over HDFS files | ? |
| Random row lookup at scale | ? |
| Import MySQL table into HDFS | ? |
| Collect logs into HDFS | ? |
| Schedule Hive and Sqoop jobs | ? |
| Batch word count over huge files | ? |

Expected:

- Hive
- HBase
- Sqoop
- Flume
- Oozie
- MapReduce

### Mini System Design Question

> You have operational data in MySQL, application logs on servers, and analysts who need daily SQL reports over Hadoop. Design a Hadoop-era pipeline.

Strong direction:

- Sqoop imports MySQL tables.
- Flume collects logs.
- HDFS stores raw data.
- Hive exposes SQL tables.
- Oozie schedules workflow.
- MapReduce/Hive jobs process data.
- Outputs are stored as partitioned tables.

### Recap Table

| Concept | Must Remember |
|---|---|
| HBase | random reads/writes by key |
| Sqoop | RDBMS to/from Hadoop bulk transfer |
| Flume | log/event ingestion into Hadoop |
| Oozie | workflow scheduler |
| Hadoop limitations | latency, small files, operations |
| Spark over MapReduce | DAG + memory + better APIs |

## Must-Know Concepts

You should be comfortable explaining:

- Hadoop as an ecosystem, not a database
- HDFS block storage
- NameNode vs DataNode
- replication factor and storage cost
- MapReduce map/shuffle/reduce
- YARN ResourceManager, NodeManager, ApplicationMaster, container
- Hive table abstraction over files
- Hive metastore as metadata catalog
- Hive partitioning vs bucketing
- HBase for key-based random access
- Sqoop for batch relational import/export
- Flume for log ingestion
- Oozie for orchestration
- Hadoop's limitations
- why Spark became more common than MapReduce

## Common Interview Questions

1. Explain Hadoop architecture.
2. How does HDFS store a large file?
3. What happens when a DataNode fails?
4. Why is NameNode critical?
5. Explain MapReduce with word count.
6. What is shuffle and why is it expensive?
7. What problem does YARN solve?
8. What is Hive and how does it differ from a traditional database?
9. What does Hive metastore store?
10. Partitioning vs bucketing in Hive?
11. Why are small files bad in Hadoop?
12. Why did Spark replace MapReduce for many workloads?

## Hands-On Project

Build a local Hadoop mental-model pipeline without installing Hadoop.

### Input

Create small log lines:

```text
2026-07-01,u1,home
2026-07-01,u2,search
2026-07-02,u1,product
```

### Steps

1. Pretend each file is stored in HDFS blocks.
2. Partition records by date.
3. Run a MapReduce-style count by page.
4. Represent a Hive external table over the partitioned data.
5. Explain what metadata would go to Hive metastore.
6. Explain how replication protects the files.
7. Explain what Oozie would schedule in production.

### What This Teaches

- HDFS storage thinking
- block and replication thinking
- MapReduce flow
- Hive table abstraction
- partition pruning
- workflow orchestration

## Production Checklist

Before designing a Hadoop-style system, ask:

- What data lands in HDFS?
- What is the expected daily data volume?
- What file format is used?
- What block size and replication factor are configured?
- Are files too small?
- What is the partition strategy?
- Does Hive metastore know all partitions?
- What jobs process the data?
- Are jobs MapReduce, Hive, Spark, or another engine?
- How are YARN queues configured?
- What happens if a DataNode fails?
- What happens if NameNode fails?
- How are workflows scheduled?
- How are failures retried?
- Are jobs idempotent?
- What is the SLA?
- Is Hadoop the right fit, or is Spark/warehouse/lakehouse better?

## Final Phase 3 Interview Answer

"Hadoop is a distributed Big Data ecosystem built around HDFS for storage, MapReduce for batch processing, and YARN for resource management. HDFS stores large files as replicated blocks across DataNodes while NameNode tracks metadata. MapReduce processes data through map, shuffle, and reduce, and YARN allocates containers across the cluster. Hive adds SQL over files using metastore metadata, partitions, and buckets. Hadoop is strong for large batch workloads, but it struggles with low latency, small files, and operational complexity, which is why Spark and modern cloud/lakehouse tools became common."
