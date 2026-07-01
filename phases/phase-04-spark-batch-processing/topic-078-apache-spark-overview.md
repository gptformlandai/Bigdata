# Topic 078: Apache Spark Overview

## 1. Goal

Understand what Apache Spark is, why it became popular, and where it fits in Big Data pipelines.

## 2. Baby Intuition

Spark is like a large team working on a big spreadsheet together.

Instead of one person reading all rows, Spark divides the data into pieces, gives pieces to many workers, and combines the results.

Compared with MapReduce, Spark is like a smarter kitchen: it plans multiple cooking steps together and can keep useful ingredients in memory instead of putting everything back into storage after every step.

## 3. What It Is

- Simple definition: Spark is a distributed engine for processing large data.
- Technical definition: Apache Spark is an open-source distributed processing engine that supports batch processing, SQL, streaming, machine learning, and graph workloads through APIs such as RDD, DataFrame, Dataset, and Spark SQL.
- Category: Distributed data processing engine.
- Related terms: driver, executor, cluster manager, DataFrame, Spark SQL, DAG, shuffle.

## 4. Why It Exists

MapReduce made large batch processing possible, but it was slow and developer-heavy for many workloads.

Problems before Spark:

- too much Java boilerplate
- disk-heavy intermediate writes
- slow multi-step pipelines
- poor fit for iterative machine learning
- less friendly SQL and Python development

Spark exists to make large data processing faster and easier.

Big Data teams care because Spark can:

- process TB/PB-scale datasets
- run ETL pipelines
- query data lakes
- train ML features
- transform files in parallel
- work with HDFS, S3, Hive, Kafka, and lakehouse tables

## 5. Where It Fits In A Data Platform

```text
Sources -> Storage/Lake -> Spark Processing -> Curated Tables -> BI/ML/Serving
```

Spark usually reads from:

- HDFS
- S3/GCS/ADLS
- Hive tables
- Parquet/ORC/Avro/CSV/JSON
- Kafka for streaming use cases

Spark writes to:

- data lakes
- warehouses
- lakehouse tables
- feature stores
- files for downstream systems

## 6. How It Works Step By Step

Simple batch job:

1. Developer writes Spark code.
2. Driver program starts.
3. Driver asks cluster manager for executors.
4. Spark reads input data in partitions.
5. Executors run tasks on partitions.
6. Spark performs transformations like filter, join, groupBy.
7. Spark writes output files/tables.
8. Failed tasks can be retried.

Mental model:

```text
code -> logical plan -> physical plan -> stages -> tasks -> output
```

## 7. How To Use It Practically

PySpark example:

```python
orders = spark.read.parquet("/data/orders")

daily_revenue = (
    orders
    .where("status = 'paid'")
    .groupBy("dt")
    .sum("amount")
)

daily_revenue.write.mode("overwrite").parquet("/data/revenue_by_day")
```

Spark submit shape:

```bash
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --num-executors 10 \
  --executor-memory 8g \
  job.py
```

## 8. Real-World Scenario

- Product/system: E-commerce analytics platform.
- Problem: Need to transform daily clickstream and orders into customer metrics.
- How Spark helps: Reads large files in parallel, joins datasets, aggregates metrics, and writes curated tables.
- What would go wrong without it: Single-machine scripts would be too slow and MapReduce would be more verbose and disk-heavy.

## 9. System Design Angle

Choose Spark when:

- data is too large for one machine
- transformations are batch or micro-batch
- SQL/DataFrame APIs are useful
- job needs parallel joins/aggregations
- pipeline has multiple transformation steps

Avoid Spark when:

- data is tiny
- simple SQL warehouse query is enough
- low-latency API serving is required
- operational overhead is not worth it

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| fast distributed processing | cluster/resource tuning |
| high-level APIs | memory/shuffle complexity |
| SQL + Python + Scala support | debugging can be non-trivial |
| works with many storage systems | small files and skew still hurt |

## 11. Failure Modes

- Failure: Executor crashes.
- Symptom: tasks fail and retry.
- Recovery: Spark reruns lost tasks.
- Prevention: memory tuning, stable nodes, good partition sizing.

- Failure: Driver crashes.
- Symptom: application fails.
- Recovery: rerun job or use platform retry.
- Prevention: avoid collecting huge data to driver.

- Failure: Shuffle too large.
- Symptom: slow job, disk spill, OOM.
- Recovery: tune partitions, reduce data before shuffle, fix skew.
- Prevention: understand joins/groupBy and data distribution.

## 12. Common Mistakes

- Mistake: Thinking Spark stores data permanently.
- Why it is wrong: Spark is mainly a compute engine; storage is HDFS/S3/tables.
- Better approach: separate compute from storage.

- Mistake: Using Spark for tiny files or tiny data.
- Why it is wrong: cluster startup/coordination overhead can dominate.
- Better approach: use SQL/Python/local processing for small work.

- Mistake: Calling `collect()` on huge data.
- Why it is wrong: it brings data to driver and can crash it.
- Better approach: write distributed output or sample.

## 13. Mini Example

Spark thinking:

```text
Input table: 1 billion rows
Partitions: 2,000
Executors: many workers
Each task processes one partition
Final result is combined/written
```

## 14. Interview Questions

1. What is Apache Spark?
2. Why did Spark become popular after MapReduce?
3. Is Spark storage or compute?
4. What are driver and executors?
5. When would you avoid Spark?

## 15. Interview Speak

"Apache Spark is a distributed compute engine for large-scale data processing. It replaced many MapReduce workloads because it supports DAG execution, in-memory computation, and high-level APIs like DataFrames and Spark SQL. Spark is compute, not storage, and it is best for large batch/ETL/SQL workloads where parallel processing is valuable."

## 16. Quick Recall

- One-line summary: Spark is distributed compute for large data.
- Three keywords: driver, executor, DataFrame.
- One trap: Treating Spark as a database.
- One memory trick: Spark is the processing team, not the warehouse.
