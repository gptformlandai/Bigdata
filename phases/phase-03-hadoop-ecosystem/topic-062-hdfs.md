# Topic 062: HDFS

## 1. Goal

Understand HDFS as Hadoop's distributed file system: what it stores, how it stores, and why it is optimized for huge files.

## 2. Baby Intuition

Think of HDFS as a giant shared warehouse for files.

Instead of putting one huge file on one shelf, HDFS breaks it into boxes and spreads those boxes across many shelves. It also keeps extra copies so one broken shelf does not lose the file.

## 3. What It Is

- Simple definition: HDFS is Hadoop's storage layer for very large files.
- Technical definition: HDFS, the Hadoop Distributed File System, stores files as replicated blocks across a cluster of DataNodes, with metadata managed by NameNode.
- Category: Distributed file system.
- Related terms: NameNode, DataNode, block, replication factor, rack awareness, namespace.

## 4. Why It Exists

Normal file systems are usually tied to one machine.

Big Data needs:

- files larger than one disk
- throughput across many disks
- automatic recovery from disk/node failure
- batch-friendly sequential reads
- cheap storage across commodity hardware

HDFS exists because one local disk cannot reliably store and serve petabyte-scale data.

## 5. Where It Fits In A Data Platform

```text
Sources -> Ingestion -> HDFS -> MapReduce/Hive/Spark -> Outputs
```

HDFS is mainly a storage layer.

It stores:

- raw logs
- CSV/JSON/Avro files
- Hive table data
- MapReduce outputs
- Spark input/output data in Hadoop-based clusters

## 6. How It Works Step By Step

Write flow:

1. Client asks NameNode where to write a file.
2. NameNode checks permissions and namespace.
3. File is split into blocks.
4. Client writes each block to a DataNode pipeline.
5. DataNodes replicate the block.
6. NameNode records block-to-DataNode metadata.
7. File becomes visible when write completes.

Read flow:

1. Client asks NameNode for block locations.
2. NameNode returns DataNodes holding each block.
3. Client reads blocks directly from nearby DataNodes.
4. Client reconstructs the file stream.

Important:

```text
NameNode stores metadata.
DataNodes store actual data blocks.
```

## 7. How To Use It Practically

Common commands:

```bash
hdfs dfs -ls /user
hdfs dfs -mkdir /user/data
hdfs dfs -put orders.csv /user/data/orders.csv
hdfs dfs -du -h /user/data
hdfs dfs -get /user/data/orders.csv .
hdfs dfs -rm /user/data/orders.csv
```

Check file blocks:

```bash
hdfs fsck /user/data/orders.csv -files -blocks -locations
```

Common production pattern:

```text
/data/raw/source_name/dt=2026-07-01/
/data/clean/source_name/dt=2026-07-01/
/data/curated/table_name/dt=2026-07-01/
```

## 8. Real-World Scenario

- Product/system: Daily log processing platform.
- Problem: Thousands of servers produce terabytes of logs every day.
- How HDFS helps: Stores log files across many nodes and lets batch jobs process them in parallel.
- What would go wrong without it: One server would run out of disk, and a disk failure could lose logs.

## 9. System Design Angle

HDFS is a good fit when:

- files are large
- workloads are batch-oriented
- reads are mostly sequential
- write once, read many times is acceptable
- high throughput matters more than low latency

HDFS is not ideal for:

- millions of tiny files
- random row-level updates
- low-latency API serving
- transactional workloads

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| huge distributed storage | NameNode metadata dependency |
| fault tolerance through replication | storage overhead |
| high throughput scans | not good for tiny files |
| data locality for compute | operational cluster management |

## 11. Failure Modes

- Failure: DataNode disk fails.
- Symptom: block replica unavailable on that disk.
- Recovery: NameNode schedules re-replication from other replicas.
- Prevention: replication, disk monitoring.

- Failure: Too many small files.
- Symptom: NameNode memory pressure and slow metadata operations.
- Recovery: compact small files into larger files.
- Prevention: write larger files and use formats like SequenceFile, Avro, Parquet, ORC.

- Failure: NameNode metadata issue.
- Symptom: clients cannot locate data.
- Recovery: standby NameNode or metadata restore.
- Prevention: HA NameNode, fsimage/edit log management.

## 12. Common Mistakes

- Mistake: Treating HDFS like a normal local file system.
- Why it is wrong: HDFS is optimized for large sequential files, not tiny random updates.
- Better approach: Use HDFS for large batch datasets.

- Mistake: Creating many tiny files.
- Why it is wrong: Each file adds metadata load to NameNode.
- Better approach: compact files and write partition-sized files.

## 13. Mini Example

If a 384 MB file uses 128 MB blocks:

```text
file block 1: 128 MB
file block 2: 128 MB
file block 3: 128 MB
```

With replication factor 3:

```text
3 logical blocks * 3 copies = 9 physical block replicas
```

## 14. Interview Questions

1. What is HDFS optimized for?
2. Why does HDFS use large block sizes?
3. What is the role of NameNode?
4. Why are small files a problem in HDFS?
5. How does HDFS recover from DataNode failure?

## 15. Interview Speak

"HDFS is Hadoop's distributed file system. It stores large files as blocks across DataNodes, while the NameNode tracks metadata. It is optimized for high-throughput sequential reads and batch processing, not low-latency random updates or many tiny files."

## 16. Quick Recall

- One-line summary: HDFS stores huge files as replicated blocks across a cluster.
- Three keywords: blocks, NameNode, DataNode.
- One trap: Using HDFS for many tiny files.
- One memory trick: HDFS is a warehouse of file blocks, not a row database.
