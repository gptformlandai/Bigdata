# Topic 100: Small Files Problem

## 1. Goal

Understand why too many small files hurt Spark and data lakes.

## 2. Baby Intuition

Reading one big book is easier than opening one million sticky notes.

Small files force Spark to do lots of tiny reads, planning, and task scheduling.

## 3. What It Is

- Simple definition: The small files problem happens when a dataset has too many tiny files.
- Technical definition: The small files problem is metadata, scheduling, and I/O overhead caused by datasets split into many files that are too small for efficient distributed processing.
- Category: Storage and performance issue.
- Related terms: file compaction, partitioning, metadata overhead, output files, task overhead.

## 4. Why It Exists

Small files happen when:

- streaming jobs write frequently
- partitioning is too granular
- many small batches land separately
- `repartition`/`coalesce` is not controlled
- each task writes its own tiny output

Spark likes parallelism, but not millions of tiny file operations.

## 5. Where It Fits In A Data Platform

```text
Data ingestion/write pattern -> many small files -> slow Spark reads/queries
```

It affects:

- HDFS
- S3/GCS/ADLS data lakes
- Hive tables
- Spark jobs
- lakehouse tables

## 6. How It Works Step By Step

Problem:

```text
1 TB dataset as 10 files -> okay, maybe not enough parallelism
1 TB dataset as 10 million tiny files -> terrible planning/open overhead
```

Spark must:

1. list files
2. create scan tasks
3. open files
4. read tiny data
5. close files
6. repeat many times

The overhead dominates actual data reading.

## 7. How To Use It Practically

Control output files:

```python
df.repartition(200).write.parquet("/output")
```

Reduce files after processing:

```python
df.coalesce(50).write.mode("overwrite").parquet("/output")
```

Avoid:

```python
df.repartition(1)
```

for large data.

Compaction idea:

```text
many small files -> rewrite into fewer larger files
```

## 8. Real-World Scenario

- Product/system: Hourly event ingestion.
- Problem: Every minute writes tiny files by country and event type.
- How small files hurt: Daily Spark jobs spend too much time listing/opening files.
- What would go wrong without compaction: queries get slower and metadata costs rise.

## 9. System Design Angle

Small files affect:

- query latency
- metadata service load
- cloud object store list operations
- Spark task overhead
- NameNode/metastore pressure

Mitigations:

- write larger batches
- compact files
- avoid over-partitioning
- tune output partition count
- use lakehouse optimize/compaction features

## 10. Trade-offs

| What We Gain From Bigger Files | What We Pay |
|---|---|
| faster scans | compaction cost |
| less metadata overhead | less immediate freshness if batching |
| fewer tasks | too few files can reduce parallelism |
| better table health | operational maintenance |

## 11. Failure Modes

- Failure: Millions of tiny files.
- Symptom: slow planning and reads.
- Recovery: compact files.
- Prevention: tune write patterns.

- Failure: Too few huge files.
- Symptom: low parallelism.
- Recovery: repartition into reasonable file count.
- Prevention: target balanced file sizes.

## 12. Common Mistakes

- Mistake: Partitioning by too many columns.
- Why it is wrong: creates many directories and tiny files.
- Better approach: partition by common filters with controlled cardinality.

- Mistake: Forcing one output file.
- Why it is wrong: one task becomes bottleneck.
- Better approach: write multiple reasonably sized files.

## 13. Mini Example

Good target for analytics often:

```text
files in hundreds of MB range
```

Exact target depends on engine, storage, and workload.

## 14. Interview Questions

1. What is the small files problem?
2. Why do small files hurt Spark?
3. How do small files happen?
4. How do you fix small files?
5. Why is `repartition(1)` bad?

## 15. Interview Speak

"The small files problem occurs when a dataset has too many tiny files, causing metadata, file open, and task scheduling overhead. Spark may spend more time planning and opening files than processing data. I fix it with compaction, better partitioning, batching writes, and controlling output partition counts."

## 16. Quick Recall

- One-line summary: Too many tiny files make big data systems slow.
- Three keywords: metadata, compaction, file size.
- One trap: `repartition(1)` for big data.
- One memory trick: Do not make Spark open a million sticky notes.
