# Topic 101: Spark Memory Management

## 1. Goal

Understand Spark memory at a practical level: why jobs spill, OOM, or slow down.

## 2. Baby Intuition

Executors have limited desk space.

They need space for:

- working on tasks
- sorting/shuffling data
- cached data
- Python/JVM overhead

If the desk is too full, work spills to the floor, or the worker crashes.

## 3. What It Is

- Simple definition: Spark memory management controls how executor memory is used for execution and storage.
- Technical definition: Spark executor memory is shared among execution memory, storage memory, user memory, overhead, and runtime needs, affecting shuffle, joins, aggregations, caching, and task stability.
- Category: Resource management/performance.
- Related terms: executor memory, memory overhead, spill, cache, garbage collection, OOM.

## 4. Why It Exists

Spark processes large data on finite machines.

Memory is needed for:

- joins
- aggregations
- sorting
- shuffling
- caching
- serialization
- Python worker processes in PySpark

If memory is insufficient, Spark spills to disk or fails.

## 5. Where It Fits In A Data Platform

```text
Executor memory -> tasks/shuffle/cache -> performance and reliability
```

Memory problems show up in:

- large joins
- groupBy
- orderBy
- cache
- skewed partitions
- collect/toPandas
- Python UDFs

## 6. How It Works Step By Step

Executor memory includes:

- execution memory: shuffle, join, sort, aggregation
- storage memory: cached data
- user memory: user objects and code
- overhead memory: JVM/native/Python/process overhead depending on deployment

When execution memory is not enough:

```text
Spark spills data to disk
```

When memory pressure is too high:

```text
executor may OOM and die
```

## 7. How To Use It Practically

Configs:

```bash
--executor-memory 8g
--executor-cores 4
--driver-memory 4g
```

Kubernetes/YARN may also need:

```text
executor memory overhead
```

Debug in Spark UI:

- spill memory
- spill disk
- executor lost
- GC time
- failed tasks
- storage tab cache size

## 8. Real-World Scenario

- Product/system: Customer join pipeline.
- Problem: Large join causes executor OOM.
- Why memory matters: one partition or join side is too large for executor memory.
- What fixes it: reduce data, broadcast small side, increase partitions, handle skew, tune memory.

## 9. System Design Angle

Memory sizing is part of architecture.

Ask:

- how large are partitions?
- how large are joins?
- how much shuffle?
- is data cached?
- are there hot keys?
- is PySpark overhead considered?

More memory is not always enough if partitioning/skew is bad.

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| more memory reduces spills | higher cost |
| caching speeds reuse | less memory for execution |
| fewer OOMs | large executors can have GC overhead |
| larger partitions reduce task overhead | higher per-task memory risk |

## 11. Failure Modes

- Failure: Executor OOM.
- Symptom: executor lost, task retries.
- Recovery: tune memory/partitions/skew.
- Prevention: avoid huge partitions and unsafe collect.

- Failure: Excessive disk spill.
- Symptom: slow stages.
- Recovery: increase memory or reduce shuffle data.
- Prevention: filter/project early.

- Failure: Cache evicts useful data.
- Symptom: recomputation and slowdown.
- Recovery: unpersist or use memory/disk persistence.
- Prevention: cache selectively.

## 12. Common Mistakes

- Mistake: Only increasing executor memory.
- Why it is wrong: skew or huge partitions may still fail.
- Better approach: fix data distribution and partition sizes.

- Mistake: Ignoring memory overhead in PySpark.
- Why it is wrong: Python processes need memory too.
- Better approach: account for overhead.

## 13. Mini Example

```text
Executor memory: 8 GB
One task tries to process 20 GB hot partition

Result:
spill heavily or fail
```

Fix:

```text
split hot partition, salt key, increase partitions, reduce data
```

## 14. Interview Questions

1. What uses executor memory?
2. What is spill?
3. Why can executor OOM happen?
4. How do caching and execution memory interact?
5. How do you debug Spark memory issues?

## 15. Interview Speak

"Spark executor memory is used for execution work like joins, shuffle, sort, and aggregation, plus storage for cached data and overhead. If memory is insufficient, Spark spills to disk or executors can OOM. I debug with Spark UI metrics like spill, GC time, executor loss, and task skew, then tune partitioning, memory, joins, and caching."

## 16. Quick Recall

- One-line summary: Spark memory is shared between work, cache, and overhead.
- Three keywords: spill, OOM, cache.
- One trap: Solving skew only by adding memory.
- One memory trick: Executor memory is desk space.
