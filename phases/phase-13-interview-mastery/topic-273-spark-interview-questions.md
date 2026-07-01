# Topic 273: Spark Interview Questions

## 1. Goal

Prepare crisp Spark answers for architecture, execution, joins, shuffle, memory, and tuning.

## 2. Baby Intuition

Spark is a distributed work planner.

You describe transformations. Spark builds a plan, splits it into tasks, runs tasks across executors, and moves data only when needed.

## 3. Must-Know Spark Concepts

- driver
- executors
- cluster manager
- DataFrame
- transformations vs actions
- lazy evaluation
- DAG
- stages and tasks
- narrow vs wide transformations
- shuffle
- joins
- partitioning
- caching
- Catalyst optimizer
- AQE

## 4. Common Questions And Strong Answers

| Question | Strong Answer |
|---|---|
| What is Spark? | distributed engine for batch, SQL, streaming, and ML-style workloads |
| Driver vs executor? | driver plans/co-ordinates; executors run tasks and store data |
| Transformation vs action? | transformations build plan; actions trigger execution |
| Lazy evaluation? | Spark waits until action to optimize full DAG |
| What is shuffle? | expensive data redistribution across partitions/nodes |

## 5. Shuffle Questions

Strong answer:

```text
Shuffle happens when data must be regrouped by key across partitions, such as groupBy, reduceByKey, distinct, sort, and many joins. It is expensive because it writes, reads, and transfers data across the network.
```

Reduce shuffle by:

- filtering early
- selecting needed columns
- using broadcast joins for small tables
- repartitioning intentionally
- avoiding unnecessary distinct/sort
- handling skew

## 6. Join Questions

| Join Type | When Used |
|---|---|
| broadcast join | one side is small enough to send to all executors |
| sort-merge join | large tables, sorted/shuffled by join key |
| shuffle hash join | hash-based join after shuffle |

Interview line:

```text
I first check table size, join key distribution, filters, and whether one side can be broadcast.
```

## 7. Data Skew Questions

Skew means a few partitions get much more data than others.

Symptoms:

- most tasks finish quickly
- a few tasks run forever
- executor memory issues
- shuffle spill

Fixes:

- salting hot keys
- broadcast smaller side
- AQE skew join handling
- pre-aggregate
- split hot keys

## 8. Cache And Persistence Questions

Use cache when:

- same DataFrame reused multiple times
- iterative logic
- expensive upstream computation

Do not cache:

- data used once
- huge data that evicts useful memory
- before filtering if filtered data is enough

## 9. Memory And Failure Questions

Common issues:

- executor OOM
- driver OOM from collect
- shuffle spill
- too many small files
- too few/too many partitions

Strong line:

```text
I avoid collect on large data, monitor Spark UI stages/tasks/shuffle/spill, and tune partitions based on data size and cluster resources.
```

## 10. Performance Tuning Checklist

1. Check Spark UI.
2. Identify slow stage.
3. Look for shuffle, skew, spill, bad join plan.
4. Filter early and prune columns.
5. Choose correct join strategy.
6. Tune partition count.
7. Cache only reused data.
8. Compact output files.
9. Use AQE when available.

## 11. Practical Interview Questions

1. A Spark job is slow. How do you debug?
2. What causes shuffle?
3. Broadcast join vs sort-merge join?
4. What is data skew and how do you fix it?
5. Why is `collect()` dangerous?
6. How do you handle small files?
7. What is AQE?
8. When should you cache?

## 12. Sample Strong Answer

Question:

```text
Your Spark job is slow. What do you do?
```

Answer:

```text
I start with the Spark UI to identify the slow stage and whether time is going into shuffle, skew, spill, or a bad join. Then I check input size, partition count, join strategy, filters, selected columns, and output file count. If one task is much slower than others, I suspect skew and use salting, AQE skew handling, or pre-aggregation. If shuffle is huge, I filter/project earlier or broadcast a small table. Finally I validate improvements with metrics, not guesses.
```

## 13. Quick Recall

- One-line summary: Spark interviews focus on execution planning, shuffle, joins, skew, and tuning.
- Three keywords: DAG, shuffle, partitions.
- One trap: saying "increase executors" before checking the Spark UI.
- Memory trick: Spark is a planner plus distributed workers.

