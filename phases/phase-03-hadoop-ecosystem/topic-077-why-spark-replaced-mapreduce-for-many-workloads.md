# Topic 077: Why Spark Replaced MapReduce For Many Workloads

## 1. Goal

Understand why Spark became preferred over MapReduce for many batch, interactive, and iterative workloads.

## 2. Baby Intuition

MapReduce is like cooking one dish, washing every utensil, putting everything away, then starting the next dish.

Spark is like keeping ingredients on the counter while cooking multiple steps.

The big idea:

```text
Spark can keep data in memory between steps.
MapReduce writes heavily to disk between steps.
```

## 3. What It Is

- Simple definition: Spark replaced MapReduce for many workloads because it is faster, easier to program, and better for multi-step data processing.
- Technical definition: Apache Spark is a distributed processing engine that supports in-memory computation, DAG execution, high-level APIs, SQL, streaming, machine learning, and graph workloads, reducing MapReduce's disk-heavy overhead.
- Category: Distributed data processing evolution.
- Related terms: RDD, DataFrame, DAG, executor, Spark SQL, caching, shuffle.

## 4. Why Spark Emerged

MapReduce was good for simple batch jobs, but painful for:

- multi-step pipelines
- iterative algorithms
- machine learning
- interactive exploration
- complex SQL
- developer productivity

MapReduce job chain:

```text
job 1 -> write to HDFS
job 2 -> read from HDFS -> write to HDFS
job 3 -> read from HDFS -> write to HDFS
```

Spark can optimize the whole graph:

```text
read -> transform -> join -> aggregate -> write
```

## 5. Where It Fits In A Data Platform

```text
Sources -> HDFS/S3/Data Lake -> Spark Processing -> Lake/Warehouse/Serving
```

Spark often replaced MapReduce as the compute engine, while still reading from:

- HDFS
- Hive tables
- S3/GCS/ADLS
- Parquet/ORC/Avro
- Kafka in streaming use cases

## 6. How It Works Step By Step

Spark high-level flow:

1. Driver program defines transformations.
2. Spark builds a DAG.
3. Execution is delayed until an action runs.
4. DAG is optimized into stages and tasks.
5. Executors run tasks across cluster.
6. Data can be cached in memory.
7. Results are written or returned.

Compared to MapReduce:

```text
MapReduce: map -> disk -> shuffle -> reduce -> disk
Spark: DAG of transformations, memory when useful, fewer forced disk boundaries
```

## 7. How To Use It Practically

PySpark example:

```python
orders = spark.read.parquet("/data/orders")

revenue = (
    orders
    .where("status = 'paid'")
    .groupBy("customer_id")
    .sum("amount")
)

revenue.write.parquet("/data/output/customer_revenue")
```

Spark SQL example:

```sql
SELECT customer_id, SUM(amount) AS revenue
FROM orders
WHERE status = 'paid'
GROUP BY customer_id;
```

## 8. Real-World Scenario

- Product/system: Recommendation training pipeline.
- Problem: Repeatedly join user events, item metadata, and model features.
- Why Spark helps: Multi-step transformations can run in one DAG and cache reused datasets.
- What would go wrong with MapReduce: Many chained jobs write/read intermediate results, making the pipeline slower and harder to maintain.

## 9. System Design Angle

Spark is better when:

- pipeline has many transformations
- data is reused
- SQL/DataFrame APIs improve productivity
- iterative ML or graph work is needed
- lower batch latency is needed

MapReduce can still be okay when:

- workload is simple
- legacy system already exists
- batch latency is not critical
- codebase is stable

Spark does not remove all hard problems:

- shuffle is still expensive
- skew still hurts
- memory tuning matters
- bad partitioning still causes pain

## 10. Trade-offs

| What Spark Improves | What We Still Pay |
|---|---|
| faster multi-step jobs | memory tuning complexity |
| higher-level APIs | cluster resource tuning |
| in-memory caching | shuffle/data skew issues |
| SQL, ML, streaming support | operational complexity |

## 11. Failure Modes

- Failure: Executor out of memory.
- Symptom: task failures and retries.
- Recovery: tune memory, partitions, caching.
- Prevention: avoid collecting huge data to driver and manage cache.

- Failure: Shuffle skew.
- Symptom: some tasks run much longer.
- Recovery: salting, skew join handling, repartitioning.
- Prevention: inspect key distribution.

- Failure: Driver failure.
- Symptom: application fails.
- Recovery: restart job depending on cluster manager.
- Prevention: stable driver resources and checkpointing when needed.

## 12. Common Mistakes

- Mistake: Thinking Spark is always magically fast.
- Why it is wrong: bad shuffles, skew, and memory pressure can make Spark slow.
- Better approach: understand DAG, partitions, caching, and shuffle.

- Mistake: Caching everything.
- Why it is wrong: memory fills and causes eviction/OOM.
- Better approach: cache only reused expensive datasets.

- Mistake: Comparing Spark only to Hadoop storage.
- Why it is wrong: Spark is compute; HDFS/S3 are storage.
- Better approach: compare Spark to MapReduce as processing engines.

## 13. Mini Example

MapReduce chain:

```text
filter job -> write output
join job -> write output
aggregate job -> write output
```

Spark DAG:

```text
filter -> join -> aggregate -> write
```

Spark can optimize the pipeline as a graph.

## 14. Interview Questions

1. Why did Spark become popular over MapReduce?
2. What does in-memory computation mean?
3. What is a DAG in Spark?
4. Does Spark eliminate shuffle cost?
5. When might MapReduce still be acceptable?

## 15. Interview Speak

"Spark replaced MapReduce for many workloads because it supports DAG execution, in-memory computation, and higher-level APIs like DataFrames and SQL. MapReduce writes intermediate results to disk between jobs, making multi-step and iterative workloads slow. Spark is faster and more productive, though shuffle, skew, and memory tuning still matter."

## 16. Quick Recall

- One-line summary: Spark improved MapReduce with DAGs, memory reuse, and better APIs.
- Three keywords: DAG, memory, DataFrame.
- One trap: Saying Spark removes all shuffle and tuning problems.
- One memory trick: MapReduce writes between steps; Spark keeps the cooking flow moving.
