# Topic 080: Driver And Executors

## 1. Goal

Understand driver and executors deeply enough to debug Spark jobs and explain distributed execution.

## 2. Baby Intuition

Driver is the brain.

Executors are the hands.

The brain decides what should happen. The hands do the actual work on pieces of data.

## 3. What It Is

- Simple definition: Driver coordinates the Spark application; executors run tasks.
- Technical definition: The driver process runs the Spark application main function and schedules work, while executor processes run tasks, hold cached data, and report results/status back to the driver.
- Category: Spark runtime components.
- Related terms: SparkSession, SparkContext, task, partition, executor memory, executor cores.

## 4. Why It Exists

Spark needs one place to:

- understand user code
- build execution plan
- track jobs/stages/tasks
- coordinate retries
- collect metadata

That is driver.

Spark also needs many workers to:

- read partitions
- run transformations
- shuffle data
- cache data
- write output

Those are executors.

## 5. Where It Fits In A Data Platform

```text
User code -> Driver -> Executors -> Storage
```

Driver is coordination.

Executors are distributed compute.

## 6. How It Works Step By Step

1. You submit a Spark app.
2. Driver starts.
3. Driver requests executors.
4. Executors start on cluster nodes.
5. Driver builds a DAG from transformations.
6. Driver splits DAG into stages and tasks.
7. Driver sends tasks to executors.
8. Executors process data partitions.
9. Executors return task status/results.
10. Driver marks job complete.

## 7. How To Use It Practically

Driver memory:

```bash
--driver-memory 4g
```

Executor memory:

```bash
--executor-memory 8g
```

Executor cores:

```bash
--executor-cores 4
```

Dangerous driver operations:

```python
df.collect()
df.toPandas()
large_list = df.rdd.map(...).collect()
```

Safer alternatives:

```python
df.write.parquet("/output/path")
df.limit(100).collect()
df.sample(0.001).show()
```

## 8. Real-World Scenario

- Product/system: Daily transaction ETL.
- Problem: Need to aggregate hundreds of millions of transactions.
- How driver/executors help: Driver coordinates plan; executors each process partitions.
- What would go wrong without separation: one process would have to plan and process everything, limiting scale.

## 9. System Design Angle

Driver failure is usually application failure.

Executor failure is often recoverable because Spark can retry tasks.

This matters for:

- long-running jobs
- streaming jobs
- expensive batch pipelines
- cluster cost
- memory tuning

Design questions:

- Is the driver doing too much?
- Are executors sized correctly?
- Are tasks balanced?
- Is data being collected to driver?

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| centralized coordination | driver can bottleneck/fail |
| parallel executor work | executor tuning needed |
| task retry | recomputation cost |
| distributed caching | memory management complexity |

## 11. Failure Modes

- Failure: Driver out of memory.
- Symptom: entire application fails.
- Recovery: rerun after fixing collect/toPandas or memory.
- Prevention: keep large data distributed.

- Failure: Executor lost.
- Symptom: tasks are retried elsewhere.
- Recovery: Spark reschedules tasks.
- Prevention: tune memory, avoid node instability.

- Failure: Too few executors.
- Symptom: slow job and underutilization.
- Recovery: increase executors if cluster allows.
- Prevention: capacity planning.

## 12. Common Mistakes

- Mistake: Using `collect()` to inspect huge data.
- Why it is wrong: it moves all data to driver.
- Better approach: use `show`, `limit`, `sample`, or write output.

- Mistake: Thinking more executor cores always helps.
- Why it is wrong: too many cores can increase contention and memory pressure.
- Better approach: tune based on workload and task behavior.

## 13. Mini Example

```text
Data has 100 partitions.
Cluster can run 20 tasks at once.

Spark runs about 20 partitions concurrently.
When they finish, next tasks start.
```

## 14. Interview Questions

1. What is the driver?
2. What is an executor?
3. Why is `collect()` risky?
4. What happens if an executor fails?
5. Why is driver failure more serious?

## 15. Interview Speak

"The driver coordinates a Spark application: it runs the main code, builds the DAG, schedules tasks, and tracks progress. Executors run tasks on data partitions and can cache data. Executor failures can often be retried, but driver failure usually fails the application."

## 16. Quick Recall

- One-line summary: Driver coordinates; executors compute.
- Three keywords: schedule, task, partition.
- One trap: Collecting huge data to driver.
- One memory trick: Driver is brain; executors are hands.
