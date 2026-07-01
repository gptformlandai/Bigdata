# Topic 064: HDFS Block Storage

## 1. Goal

Understand why HDFS splits files into large blocks and how that enables distributed storage and parallel processing.

## 2. Baby Intuition

If a pizza is too large for one person, you slice it.

If a file is too large for one machine, HDFS slices it into blocks.

Each block can live on a different machine and be processed separately.

## 3. What It Is

- Simple definition: HDFS block storage means large files are split into fixed-size chunks called blocks.
- Technical definition: HDFS stores files as blocks, commonly 128 MB or 256 MB, distributed and replicated across DataNodes.
- Category: Distributed storage layout.
- Related terms: block size, replica, split, data locality, parallelism.

## 4. Why It Exists

Large blocks solve several problems:

- one huge file can span many machines
- different parts of a file can be processed in parallel
- metadata stays manageable
- disk reads become efficient sequential reads
- failed blocks can be replicated independently

Small blocks would create too much metadata and overhead.

## 5. Where It Fits In A Data Platform

```text
Large files -> HDFS blocks -> DataNodes -> processing tasks
```

Blocks sit below tools like:

- MapReduce
- Hive
- Spark on Hadoop
- HBase HFiles internally in HDFS-backed setups

## 6. How It Works Step By Step

Example: write a 300 MB file with 128 MB block size.

1. Client writes file.
2. HDFS creates block 1: 128 MB.
3. HDFS creates block 2: 128 MB.
4. HDFS creates block 3: 44 MB.
5. Each block is placed on DataNodes.
6. Each block is replicated.
7. Processing engines can assign tasks per block or split.

Visual:

```text
orders.log 300 MB
  -> block 1: 128 MB
  -> block 2: 128 MB
  -> block 3: 44 MB
```

## 7. How To Use It Practically

Check block information:

```bash
hdfs fsck /data/orders.log -files -blocks -locations
```

Common block sizes:

```text
128 MB
256 MB
512 MB in some large clusters
```

You usually do not tune block size first. First understand:

- file size
- query pattern
- processing engine
- NameNode metadata load

## 8. Real-World Scenario

- Product/system: Daily web log analytics.
- Problem: Each day produces multi-TB log files.
- How blocks help: Split files into blocks so many workers can process different parts in parallel.
- What would go wrong without it: One huge file would be tied to one machine and processing would be slow.

## 9. System Design Angle

Block storage helps with:

- horizontal scaling
- parallel reads
- fault isolation
- throughput
- data locality

But block storage is not enough by itself.

You still need:

- good file sizes
- good partitioning
- appropriate file formats
- enough cluster resources

Interview note:

```text
HDFS block is a storage unit.
MapReduce input split is a processing unit.
They are related but not always identical.
```

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| parallel processing | block metadata to track |
| large sequential reads | poor tiny-file behavior |
| independent replication | storage overhead |
| easier recovery | block placement complexity |

## 11. Failure Modes

- Failure: Block replica lost.
- Symptom: under-replicated block.
- Recovery: copy from another replica.
- Prevention: replication factor and monitoring.

- Failure: Too many blocks.
- Symptom: NameNode metadata pressure.
- Recovery: increase block size or compact files.
- Prevention: write larger files.

- Failure: Bad block placement.
- Symptom: poor data locality or rack risk.
- Recovery: balancer and re-replication.
- Prevention: rack-aware placement.

## 12. Common Mistakes

- Mistake: Thinking HDFS block size is same as OS disk block size.
- Why it is wrong: HDFS blocks are much larger and managed by HDFS.
- Better approach: Treat HDFS blocks as distributed file chunks.

- Mistake: Using tiny files because "HDFS can store files."
- Why it is wrong: tiny files create too many metadata entries and inefficient processing.
- Better approach: batch small records into larger files.

## 13. Mini Example

If block size is 128 MB:

```text
10 MB file -> 1 block
128 MB file -> 1 block
129 MB file -> 2 blocks
1 GB file -> 8 blocks
```

## 14. Interview Questions

1. Why does HDFS use large blocks?
2. How does block size affect parallelism?
3. What happens if a block replica is lost?
4. Why are tiny files bad in HDFS?
5. What is the difference between a block and an input split?

## 15. Interview Speak

"HDFS stores files as large blocks spread across DataNodes. This lets huge files exceed one machine's disk and enables parallel processing. Large blocks reduce metadata overhead and support high-throughput sequential reads, but HDFS performs poorly with many tiny files."

## 16. Quick Recall

- One-line summary: HDFS blocks are large chunks of files stored across the cluster.
- Three keywords: block, split, parallelism.
- One trap: Confusing HDFS block with tiny OS blocks.
- One memory trick: Big file becomes slices; workers process slices.
