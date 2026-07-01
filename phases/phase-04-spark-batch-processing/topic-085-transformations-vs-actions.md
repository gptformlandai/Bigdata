# Topic 085: Transformations Vs Actions

## 1. Goal

Understand the difference between transformations that build a Spark plan and actions that actually run it.

## 2. Baby Intuition

Transformations are like writing a recipe.

Actions are like actually cooking.

Until you perform an action, Spark mostly remembers what should happen, but does not execute the full work.

## 3. What It Is

- Simple definition: Transformations describe new data; actions trigger computation.
- Technical definition: Transformations create new RDD/DataFrame logical plans lazily, while actions execute the plan and return results or write output.
- Category: Spark execution concept.
- Related terms: lazy evaluation, DAG, job, stage, task.

## 4. Why It Exists

Spark waits before running so it can:

- see the full chain of operations
- optimize the plan
- combine steps
- avoid unnecessary work
- schedule efficiently

If Spark ran every line immediately, it would lose many optimization opportunities.

## 5. Where It Fits In A Data Platform

```text
Read -> transformations build plan -> action triggers job -> write/output
```

Most ETL code is many transformations followed by one or more actions.

## 6. How It Works Step By Step

Example:

```python
df = spark.read.parquet("/data/orders")
paid = df.where("status = 'paid'")
revenue = paid.groupBy("customer_id").sum("amount")
```

So far:

```text
Spark built a plan.
No full scan has necessarily happened.
```

Action:

```python
revenue.write.parquet("/data/revenue")
```

Now Spark runs the job.

## 7. How To Use It Practically

Common transformations:

- `select`
- `filter` / `where`
- `withColumn`
- `groupBy`
- `join`
- `orderBy`
- `repartition`
- `dropDuplicates`

Common actions:

- `count`
- `show`
- `collect`
- `take`
- `write`
- `foreach`

Danger:

```python
df.count()
df.write.parquet("/output")
```

This can run two separate jobs unless cached or optimized by the platform.

## 8. Real-World Scenario

- Product/system: Daily revenue ETL.
- Problem: Build several filtering and aggregation steps.
- How this helps: Transformations describe the pipeline; one write action runs it.
- What would go wrong without understanding it: You may accidentally trigger multiple expensive jobs with repeated actions.

## 9. System Design Angle

Actions matter because they define job boundaries.

Too many actions can:

- recompute work
- increase cost
- increase runtime
- cause duplicate side effects

Production habit:

```text
Minimize unnecessary actions in the middle of a pipeline.
```

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| optimizer sees whole plan | execution can feel non-obvious |
| avoids unnecessary work | debugging needs Spark UI |
| efficient scheduling | accidental actions can be costly |

## 11. Failure Modes

- Failure: Action triggers huge collect.
- Symptom: driver OOM.
- Recovery: rerun with safer action.
- Prevention: use write, limit, sample.

- Failure: Multiple actions recompute same lineage.
- Symptom: job runs same expensive steps repeatedly.
- Recovery: cache/persist if reused.
- Prevention: inspect action placement.

## 12. Common Mistakes

- Mistake: Thinking `filter` immediately scans data.
- Why it is wrong: it is lazy.
- Better approach: remember actions trigger execution.

- Mistake: Calling `count()` everywhere for debugging.
- Why it is wrong: each count may trigger a full job.
- Better approach: use limited samples and Spark UI.

## 13. Mini Example

```python
filtered = df.filter("amount > 100")  # transformation
filtered.count()                      # action
```

## 14. Interview Questions

1. What is a transformation?
2. What is an action?
3. Why is Spark lazy?
4. Give examples of transformations and actions.
5. Why can repeated actions be expensive?

## 15. Interview Speak

"Transformations build a lazy plan and actions trigger execution. For example, filter and join are transformations, while count, collect, and write are actions. This laziness lets Spark optimize the plan, but repeated actions can recompute expensive work."

## 16. Quick Recall

- One-line summary: Transformations plan; actions run.
- Three keywords: lazy, plan, trigger.
- One trap: Calling many actions accidentally.
- One memory trick: Recipe vs cooking.
