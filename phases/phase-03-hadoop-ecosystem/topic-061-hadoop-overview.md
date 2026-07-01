# Topic 061: Hadoop Overview

## 1. Goal

Understand what Hadoop is, why it was created, and why its ideas still matter even when modern teams use Spark, cloud storage, and lakehouse tools.

## 2. Baby Intuition

Imagine you have one giant book so large that one person cannot carry it or read it quickly.

Hadoop says:

- tear the book into many chunks
- put chunks on many shelves
- ask many people to read their local chunks in parallel
- combine the answers

That is the heart of Hadoop: distributed storage plus distributed batch processing.

## 3. What It Is

- Simple definition: Hadoop is a system for storing and processing huge datasets across many machines.
- Technical definition: Apache Hadoop is an open-source framework that provides distributed storage through HDFS and distributed processing/resource management through MapReduce and YARN.
- Category: Big Data storage and batch processing ecosystem.
- Related terms: HDFS, MapReduce, YARN, Hive, cluster, commodity hardware, data locality.

## 4. Why It Exists

Before Hadoop, many systems assumed data fit on one powerful machine or expensive storage appliance.

That broke when companies needed to process:

- web crawl data
- search logs
- clickstream events
- machine logs
- recommendation data
- large analytical datasets

The problem:

```text
Data became too large for one machine to store and process cheaply.
```

Hadoop solved this by using many cheaper machines together.

Big Data teams care because Hadoop introduced mental models that still matter:

- distribute files
- replicate data
- move compute near data
- recover from node failure
- process in parallel

## 5. Where It Fits In A Data Platform

```text
Sources -> Ingestion -> HDFS Storage -> MapReduce/Hive Processing -> Reports/Exports
```

Typical Hadoop-era architecture:

```text
Application logs / DB exports / clickstream
  -> ingest into HDFS
  -> process with MapReduce or Hive
  -> write cleaned/aggregated data back to HDFS
  -> query or export results
```

Upstream systems:

- application logs
- relational databases
- web servers
- batch files
- event collectors

Downstream systems:

- Hive tables
- dashboards
- machine learning jobs
- exports to databases
- reporting systems

## 6. How It Works Step By Step

At a high level:

1. A large file is uploaded to HDFS.
2. HDFS splits the file into blocks.
3. Blocks are stored across DataNodes.
4. Blocks are replicated for fault tolerance.
5. A processing job is submitted.
6. YARN allocates cluster resources.
7. MapReduce tasks process blocks in parallel.
8. Results are written back to HDFS.

Simple flow:

```text
Huge file
  -> HDFS blocks
  -> parallel map tasks
  -> shuffle/sort
  -> reduce tasks
  -> output files
```

## 7. How To Use It Practically

Common Hadoop command style:

```bash
hdfs dfs -ls /
hdfs dfs -mkdir /data
hdfs dfs -put local_file.csv /data/
hdfs dfs -cat /data/local_file.csv
hdfs dfs -rm /data/local_file.csv
```

You do not need to memorize every command now. Learn the pattern:

```text
hdfs dfs <file-system-command>
```

Hadoop is usually operated as a cluster, not a small local script.

## 8. Real-World Scenario

- Product/system: Search engine log analytics.
- Problem: Billions of search queries and clicks need batch analysis.
- How Hadoop helps: Store logs cheaply in HDFS and run large parallel jobs to compute ranking signals, trends, and quality metrics.
- What would go wrong without it: One machine would run out of disk, processing would be too slow, and hardware failures would break long jobs.

## 9. System Design Angle

Choose Hadoop-like architecture when:

- data is very large
- batch processing is acceptable
- throughput matters more than low latency
- storage cost matters
- data can be processed in parallel

Avoid Hadoop for:

- millisecond APIs
- small datasets
- interactive low-latency queries without extra engines
- frequent random row updates

System design trade-off:

```text
Hadoop gives scale and fault tolerance, but not low-latency interactivity.
```

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| cheap horizontal scale | operational complexity |
| fault-tolerant storage | storage overhead from replication |
| parallel batch processing | high latency for jobs |
| data locality | less useful in cloud object storage era |

## 11. Failure Modes

- Failure: DataNode dies.
- Symptom: Some blocks temporarily unavailable from that node.
- Recovery: HDFS reads replicas from other DataNodes and re-replicates blocks.
- Prevention: replication factor, monitoring, disk health checks.

- Failure: NameNode unavailable.
- Symptom: clients cannot locate files or blocks.
- Recovery: failover to standby NameNode in high-availability setup.
- Prevention: NameNode HA, checkpoints, metadata backups.

- Failure: MapReduce task fails.
- Symptom: job slows or retries task.
- Recovery: task reruns on another node.
- Prevention: retries, input validation, resource tuning.

## 12. Common Mistakes

- Mistake: Thinking Hadoop is one tool.
- Why it is wrong: Hadoop is an ecosystem: HDFS, MapReduce, YARN, Hive, and more.
- Better approach: Separate storage, compute, resource management, and SQL layers.

- Mistake: Thinking Hadoop is always the best modern choice.
- Why it is wrong: Cloud storage, Spark, lakehouses, and warehouses often replaced classic Hadoop clusters.
- Better approach: Learn Hadoop concepts, then understand modern alternatives.

## 13. Mini Example

Mental model:

```text
1 TB file on one machine:
  one reader, slow, fragile

1 TB file split across 100 machines:
  many readers, faster, fault-tolerant
```

## 14. Interview Questions

1. What problem did Hadoop solve?
2. What are the main components of Hadoop?
3. Why does Hadoop split files into blocks?
4. Why is Hadoop better for batch than real-time serving?
5. How does Hadoop handle machine failure?

## 15. Interview Speak

"Hadoop is a distributed Big Data framework built around HDFS for storage and MapReduce/YARN for processing and resource management. It was designed to store and process huge datasets across many commodity machines. It is strong for large batch workloads and fault tolerance, but less ideal for low-latency interactive workloads."

## 16. Quick Recall

- One-line summary: Hadoop stores and processes huge data across many machines.
- Three keywords: HDFS, MapReduce, YARN.
- One trap: Calling Hadoop a database.
- One memory trick: Big file -> many blocks -> many machines -> parallel processing.
