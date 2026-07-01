# Topic 093: Partitioning In Spark

## 1. Goal

Understand partitions as the units of parallelism in Spark.

## 2. Baby Intuition

A partition is a slice of data.

Spark gives slices to workers. More slices means more tasks, but too many tiny slices create overhead.

## 3. What It Is

- Simple definition: A Spark partition is a chunk of distributed data processed by a task.
- Technical definition: Spark partitions are logical divisions of an RDD/DataFrame that determine task parallelism and data distribution across executors.
- Category: Parallelism and data layout.
- Related terms: task, executor, repartition, coalesce, shuffle partition.

## 4. Why It Exists

Spark needs to split data so many cores can work in parallel.

Partitions decide:

- how many tasks are created
- how data is distributed
- how much data one task processes
- whether cluster resources are used efficiently

## 5. Where It Fits In A Data Platform

```text
Files/Table -> Spark partitions -> tasks -> executors
```

Partitioning exists in:

- input file splits
- DataFrame partitions
- shuffle partitions
- output files

## 6. How It Works Step By Step

Example:

```text
DataFrame has 200 partitions.
Spark creates 200 tasks for a stage.
```

If cluster can run 40 tasks at once:

```text
5 waves of tasks
```

Repartition:

```python
df2 = df.repartition(400, "customer_id")
```

This creates 400 partitions by customer id and causes shuffle.

Coalesce:

```python
df2 = df.coalesce(50)
```

This reduces partitions, usually with less shuffle.

## 7. How To Use It Practically

Check partitions:

```python
df.rdd.getNumPartitions()
```

Change partitions:

```python
df.repartition(200)
df.repartition("customer_id")
df.coalesce(20)
```

Tune shuffle partitions:

```python
spark.conf.set("spark.sql.shuffle.partitions", "200")
```

## 8. Real-World Scenario

- Product/system: Daily ETL over 2 TB of data.
- Problem: Job is slow because only 20 partitions exist, underusing the cluster.
- How partitioning helps: Increase partitions so more tasks run in parallel.
- What would go wrong with too many partitions: overhead and many tiny output files.

## 9. System Design Angle

Good partitioning balances:

- parallelism
- task size
- shuffle cost
- output file size
- skew

Rules of thumb vary, but useful thinking:

```text
too few partitions -> underutilized cluster
too many partitions -> scheduling overhead and small files
skewed partitions -> straggler tasks
```

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| more parallelism | more task overhead |
| better distribution | repartition causes shuffle |
| control output files | wrong count creates tiny files |
| key-based layout | skew risk |

## 11. Failure Modes

- Failure: One huge partition.
- Symptom: one task runs forever or OOMs.
- Recovery: repartition or fix skew.
- Prevention: inspect partition sizes.

- Failure: Too many partitions.
- Symptom: scheduler overhead and small files.
- Recovery: coalesce before write.
- Prevention: set sane partition counts.

- Failure: Repartition by skewed key.
- Symptom: hot partitions.
- Recovery: salting/AQE/skew handling.
- Prevention: profile key cardinality.

## 12. Common Mistakes

- Mistake: Using `repartition(1)` for one output file.
- Why it is wrong: forces all data to one task and can OOM.
- Better approach: write multiple files or use downstream compaction.

- Mistake: Thinking partitioning always means Hive partitions.
- Why it is wrong: Spark partitions are execution chunks; Hive partitions are storage folders.
- Better approach: distinguish compute partitions vs table partitions.

## 13. Mini Example

```text
100 GB data / 100 partitions = about 1 GB per partition
100 GB data / 10,000 partitions = about 10 MB per partition
```

Both can be wrong depending on workload.

## 14. Interview Questions

1. What is a Spark partition?
2. How does partition count affect parallelism?
3. Repartition vs coalesce?
4. Why is `repartition(1)` dangerous?
5. Spark partitions vs Hive partitions?

## 15. Interview Speak

"Spark partitions are chunks of data processed by tasks. Partition count controls parallelism and task size. Too few partitions underutilize the cluster, too many add scheduling overhead and small files, and skewed partitions create stragglers. `repartition` shuffles, while `coalesce` usually reduces partitions with less movement."

## 16. Quick Recall

- One-line summary: Spark partitions are task-sized chunks of data.
- Three keywords: task, parallelism, skew.
- One trap: `repartition(1)` on big data.
- One memory trick: Partitions are slices of the pizza.
