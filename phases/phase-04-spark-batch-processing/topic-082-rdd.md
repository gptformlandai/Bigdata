# Topic 082: RDD

## 1. Goal

Understand RDDs as Spark's original low-level distributed data abstraction.

## 2. Baby Intuition

An RDD is like a huge list split across many machines.

Each machine holds a piece of the list. Spark knows how to transform each piece and rebuild lost pieces if needed.

## 3. What It Is

- Simple definition: RDD is a distributed collection of data.
- Technical definition: RDD, Resilient Distributed Dataset, is an immutable, partitioned collection of records that can be processed in parallel and recomputed through lineage after failure.
- Category: Low-level Spark API.
- Related terms: partition, lineage, transformation, action, fault tolerance, immutable.

## 4. Why It Exists

Spark needed a core abstraction for:

- distributed data
- parallel operations
- fault recovery
- lazy transformations
- memory caching

RDD was the original answer.

RDD stands for:

```text
Resilient: can recover from failure
Distributed: split across cluster
Dataset: collection of records
```

## 5. Where It Fits In A Data Platform

```text
Storage -> RDD transformations -> Output
```

RDDs are lower level than DataFrames.

Today, most production Spark ETL uses DataFrames/Spark SQL, but RDD knowledge helps understand Spark internals.

## 6. How It Works Step By Step

Example:

```python
rdd = sc.textFile("/data/logs")
words = rdd.flatMap(lambda line: line.split())
pairs = words.map(lambda word: (word, 1))
counts = pairs.reduceByKey(lambda a, b: a + b)
```

What happens:

1. `textFile` creates RDD from files.
2. `flatMap` defines transformation.
3. `map` defines transformation.
4. `reduceByKey` defines grouped aggregation.
5. Nothing actually runs yet.
6. An action like `collect()` or `saveAsTextFile()` triggers execution.

## 7. How To Use It Practically

RDD example:

```python
lines = sc.parallelize(["hello spark", "hello data"])

counts = (
    lines
    .flatMap(lambda line: line.split())
    .map(lambda word: (word, 1))
    .reduceByKey(lambda left, right: left + right)
)

print(counts.collect())
```

When to use RDDs:

- custom low-level transformations
- unstructured records
- libraries requiring RDD API
- learning Spark internals

Prefer DataFrames for:

- SQL
- structured data
- optimization
- production ETL

## 8. Real-World Scenario

- Product/system: Custom log parser.
- Problem: Logs are irregular and need custom parsing before becoming structured.
- How RDD helps: Allows custom record-by-record parsing.
- What would go wrong without it: DataFrame schema may be hard to apply before parsing.

## 9. System Design Angle

RDDs give control but lose many optimizer benefits.

DataFrames allow Catalyst to optimize:

- projection pruning
- filter pushdown
- join strategy
- physical execution

RDDs are harder for Spark to optimize because logic is opaque functions.

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| low-level control | less automatic optimization |
| custom transformations | more verbose code |
| lineage-based recovery | harder schema handling |
| works for unstructured data | fewer SQL benefits |

## 11. Failure Modes

- Failure: Long lineage chain.
- Symptom: recomputation becomes expensive after failure.
- Recovery: checkpoint.
- Prevention: checkpoint long iterative jobs.

- Failure: Bad lambda serialization.
- Symptom: task serialization errors.
- Recovery: fix closure/code dependencies.
- Prevention: avoid capturing huge/unserializable objects.

- Failure: Collect huge RDD.
- Symptom: driver OOM.
- Recovery: rerun safely.
- Prevention: save distributed output or sample.

## 12. Common Mistakes

- Mistake: Using RDDs for all structured ETL.
- Why it is wrong: DataFrames are optimized and easier for SQL-like work.
- Better approach: use DataFrames unless low-level control is needed.

- Mistake: Forgetting RDDs are immutable.
- Why it is wrong: transformations create new RDDs.
- Better approach: think functional transformations.

## 13. Mini Example

```text
RDD partitions:
partition 0: records 1-1000
partition 1: records 1001-2000
partition 2: records 2001-3000
```

Each partition can be processed by a task.

## 14. Interview Questions

1. What is an RDD?
2. What does resilient mean in RDD?
3. Why are RDDs immutable?
4. RDD vs DataFrame?
5. When would you still use RDDs?

## 15. Interview Speak

"An RDD is Spark's original low-level abstraction: an immutable distributed collection split into partitions. It is fault tolerant through lineage, meaning Spark can recompute lost partitions. Today, DataFrames are preferred for structured workloads because Catalyst can optimize them."

## 16. Quick Recall

- One-line summary: RDD is an immutable distributed collection with lineage.
- Three keywords: resilient, partitioned, lineage.
- One trap: Using RDD when DataFrame optimization is better.
- One memory trick: RDD is a split list Spark can rebuild.
