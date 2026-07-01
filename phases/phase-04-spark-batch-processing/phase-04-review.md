# Phase 4 Review: Spark And Batch Processing

This review checks whether you understand Spark from beginner mental model to production debugging and interview communication.

## Phase Summary

Phase 4 covered:

- Spark overview and architecture
- driver, executors, and cluster managers
- RDD, DataFrame, Dataset
- transformations, actions, lazy evaluation, DAG
- stages, tasks, narrow/wide transformations, shuffle
- broadcast join and sort-merge join
- partitioning, caching, Spark SQL
- Catalyst, Tungsten, AQE
- data skew, small files, memory, tuning, failure handling
- PySpark and Spark deployment on Kubernetes/cloud platforms

Main idea:

```text
Spark is a distributed compute engine. Performance depends on plans, partitions, shuffle, joins, memory, and data layout.
```

## Checkpoint 1: Topics 078-084

Topics:

- Apache Spark overview
- Spark architecture
- Driver and executors
- Spark cluster manager
- RDD
- DataFrame
- Dataset

### Quiz

1. Is Spark compute or storage?
2. What does the driver do?
3. What do executors do?
4. What is the role of cluster manager?
5. Why are DataFrames preferred over RDDs for structured data?

### Practical Exercise

Explain this architecture in your own words:

```text
spark-submit -> cluster manager -> driver -> executors -> tasks -> storage
```

### Mini System Design Question

> You need to process 5 TB of daily clickstream files and write customer metrics. Where does Spark fit?

Strong direction:

- Spark is the processing layer.
- Data lives in HDFS/S3/lake.
- Driver coordinates.
- Executors process partitions.
- Output is written to curated tables.

### Recap Table

| Concept | Must Remember |
|---|---|
| Spark | distributed compute engine |
| Driver | plans and schedules |
| Executor | runs tasks |
| Cluster manager | allocates resources |
| RDD | low-level distributed collection |
| DataFrame | distributed optimized table |
| Dataset | typed structured API in Scala/Java |

## Checkpoint 2: Topics 085-094

Topics:

- Transformations vs actions
- Lazy evaluation
- DAG
- Stages and tasks
- Narrow vs wide transformations
- Shuffle
- Broadcast join
- Sort-merge join
- Partitioning in Spark
- Caching and persistence

### Quiz

1. What triggers Spark execution?
2. Why is Spark lazy?
3. What creates a stage boundary?
4. Why is shuffle expensive?
5. When should you use broadcast join?
6. Repartition vs coalesce?
7. When should you cache?

### Practical Exercise

For this pipeline, identify transformations, actions, and shuffle points:

```python
orders = spark.read.parquet("/orders")
paid = orders.filter("status = 'paid'")
joined = paid.join(customers, "customer_id")
result = joined.groupBy("region").sum("amount")
result.write.parquet("/out")
```

### Mini System Design Question

> A Spark job joins a 2 TB fact table with a 5 MB lookup table. What join strategy should you consider?

Strong direction:

- Broadcast the 5 MB lookup table.
- Avoid shuffling the 2 TB fact table.
- Confirm executor memory can hold broadcast data.
- Inspect plan.

### Recap Table

| Concept | Must Remember |
|---|---|
| Transformation | builds plan |
| Action | triggers execution |
| DAG | dependency graph |
| Stage | group of tasks split by shuffle |
| Task | unit of work per partition |
| Shuffle | expensive data movement |
| Broadcast join | small table copied to executors |
| Cache | reuse expensive data |

## Checkpoint 3: Topics 095-103

Topics:

- Spark SQL
- Catalyst optimizer
- Tungsten engine
- Adaptive query execution
- Data skew
- Small files problem
- Spark memory management
- Spark performance tuning
- Spark job failure handling

### Quiz

1. What does Catalyst optimize?
2. What does Tungsten improve?
3. What can AQE change at runtime?
4. How do you detect data skew?
5. Why are small files bad?
6. What causes executor OOM?
7. How do you tune a slow Spark job?

### Practical Exercise

Given a slow Spark job:

```text
Stage 12 takes 90 minutes.
One task reads 70 GB shuffle data.
Most other tasks read less than 500 MB.
```

Answer:

- What is the likely problem?
- How would you confirm it?
- What fixes would you try?

Expected:

- likely data skew
- confirm with Spark UI and key distribution
- use salting, AQE skew join, pre-aggregation, better partition key, or special handling for hot keys

### Mini System Design Question

> A daily ETL table has millions of tiny Parquet files and Spark queries are slow. What do you do?

Strong direction:

- Identify small files problem.
- Compact files.
- Reduce over-partitioning.
- Tune output partitions.
- Use table maintenance/OPTIMIZE if available.
- Avoid `repartition(1)`.

### Recap Table

| Concept | Must Remember |
|---|---|
| Spark SQL | SQL over distributed data |
| Catalyst | query optimizer |
| Tungsten | execution optimization |
| AQE | runtime plan adaptation |
| Skew | one/few tasks get too much data |
| Small files | metadata/open/task overhead |
| Memory | execution + cache + overhead |
| Failure handling | retries plus idempotent outputs |

## Checkpoint 4: Topics 104-106

Topics:

- PySpark
- Spark on Kubernetes
- Spark on EMR/Dataproc/Databricks

### Quiz

1. What is PySpark?
2. Why is `toPandas()` dangerous on large data?
3. How does Spark run on Kubernetes?
4. What do managed Spark platforms provide?
5. Does managed Spark remove the need for tuning?

### Practical Exercise

Write a PySpark job outline:

- read Parquet
- filter paid orders
- group by date
- write output
- avoid collect

### Mini System Design Question

> Your company is cloud-first and wants scheduled Spark ETL with minimal cluster operations. What options do you consider?

Strong direction:

- EMR on AWS, Dataproc on GCP, Databricks lakehouse platform, or Spark on Kubernetes.
- Compare cloud provider, governance, cost, scaling, notebooks/jobs, and table format needs.

### Recap Table

| Concept | Must Remember |
|---|---|
| PySpark | Python API for Spark |
| Spark on Kubernetes | driver/executors as pods |
| EMR | AWS managed Spark/Hadoop |
| Dataproc | GCP managed Spark/Hadoop |
| Databricks | managed Spark/lakehouse platform |

## Must-Know Concepts

You should be comfortable explaining:

- Spark as compute, not storage
- driver vs executor
- cluster manager role
- RDD vs DataFrame vs Dataset
- transformations vs actions
- lazy evaluation
- DAG, stages, tasks
- narrow vs wide transformations
- shuffle cost
- broadcast join vs sort-merge join
- partitioning, repartition, coalesce
- cache/persist/unpersist
- Spark SQL and Catalyst
- Tungsten and code generation
- AQE
- skew detection and salting
- small files and compaction
- memory, spill, OOM
- Spark UI debugging
- idempotent Spark writes
- PySpark pitfalls
- managed Spark deployment trade-offs

## Common Interview Questions

1. Why did Spark replace MapReduce for many workloads?
2. Explain Spark architecture.
3. Driver vs executor?
4. What is lazy evaluation?
5. What is a DAG?
6. What are stages and tasks?
7. Narrow vs wide transformation?
8. What is shuffle and why is it expensive?
9. Broadcast join vs sort-merge join?
10. How do you handle data skew?
11. How do you fix small files?
12. How do you tune a slow Spark job?
13. Why is `collect()` dangerous?
14. What does Catalyst do?
15. What is AQE?

## Hands-On Project

Build a local Spark mental-model simulator.

### Input

Use small order records:

```text
order_id,customer_id,amount,status,country
o1,c1,10,paid,US
o2,c1,15,paid,US
o3,c2,5,failed,IN
o4,c3,20,paid,US
```

### Steps

1. Split records into partitions.
2. Apply a filter transformation.
3. Apply a map/select transformation.
4. Simulate a groupBy shuffle by customer.
5. Reduce totals per customer.
6. Add a tiny country lookup table and simulate broadcast join.
7. Add skew by making many `US` records.
8. Explain how Spark UI would show skew.

### What This Teaches

- partitions
- transformations
- actions
- shuffle
- groupBy
- broadcast join
- skew

## Production Checklist

Before shipping a Spark job, ask:

- What data does it read?
- What file format?
- How many files?
- Are files too small?
- What partitions exist?
- Does query filter partition columns?
- What transformations are narrow vs wide?
- Where are shuffles?
- What join strategies are used?
- Can any small table be broadcast?
- Is there key skew?
- What is `spark.sql.shuffle.partitions`?
- Does the job cache anything?
- Is cache reused and unpersisted?
- Are there Python UDFs?
- Are built-in functions possible?
- Is output idempotent?
- What happens on failure/rerun?
- What does Spark UI show?
- What is the SLA?
- What is the cluster cost?

## Final Phase 4 Interview Answer

"Spark is a distributed compute engine for large-scale ETL, SQL, and batch processing. A driver builds the plan and schedules work, executors run tasks on partitions, and a cluster manager allocates resources. Spark is lazy: transformations build a DAG and actions trigger jobs. Performance depends heavily on shuffle, joins, partitioning, skew, caching, file layout, and memory. I debug with Spark UI and explain plans, then tune using filter/projection pushdown, broadcast joins, AQE, partition tuning, skew handling, compaction, and safe/idempotent writes."
