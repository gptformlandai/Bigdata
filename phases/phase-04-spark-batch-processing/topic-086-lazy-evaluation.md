# Topic 086: Lazy Evaluation

## 1. Goal

Understand why Spark waits to execute transformations and how lazy evaluation improves optimization.

## 2. Baby Intuition

Spark does not start driving after every direction.

It waits until it sees the whole route, then chooses a better path.

## 3. What It Is

- Simple definition: Lazy evaluation means Spark delays execution until an action is called.
- Technical definition: Spark records transformations as a lineage/logical plan and only executes them when an action requires a result.
- Category: Execution optimization concept.
- Related terms: transformation, action, lineage, DAG, Catalyst, job.

## 4. Why It Exists

Lazy evaluation lets Spark:

- optimize across multiple steps
- push filters closer to data source
- read only needed columns
- collapse operations
- avoid running unused branches
- schedule work as stages

Without laziness, every transformation would run immediately and write/read unnecessary intermediate data.

## 5. Where It Fits In A Data Platform

```text
ETL code -> lazy plan -> optimized execution -> output table
```

Lazy evaluation affects all Spark jobs:

- RDD
- DataFrame
- Spark SQL

## 6. How It Works Step By Step

Code:

```python
df = spark.read.parquet("/orders")
paid = df.filter("status = 'paid'")
selected = paid.select("customer_id", "amount")
```

No full job yet.

Action:

```python
selected.write.parquet("/paid_orders")
```

Now Spark:

1. analyzes the plan
2. optimizes it
3. creates physical execution
4. schedules tasks
5. writes output

## 7. How To Use It Practically

Use `explain()` to inspect plans:

```python
selected.explain(True)
```

You can see:

- parsed logical plan
- analyzed logical plan
- optimized logical plan
- physical plan

Debug carefully:

```python
df.show(5)
```

`show()` is an action. It triggers work.

## 8. Real-World Scenario

- Product/system: Lakehouse ETL.
- Problem: Read wide Parquet table but only need 5 columns and one date.
- How lazy evaluation helps: Spark can push projection/filter into the scan.
- What would go wrong without it: Spark might read and process unnecessary data.

## 9. System Design Angle

Lazy evaluation helps with cost and performance.

But it means:

- errors may appear later than the line where transformation was written
- repeated actions can rerun lineage
- debugging requires understanding action boundaries

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| better optimization | delayed errors |
| fewer unnecessary scans | debugging less intuitive |
| whole-plan scheduling | accidental recomputation |

## 11. Failure Modes

- Failure: Error appears only at action.
- Symptom: code seems fine until `write` or `count`.
- Recovery: inspect schema and plan earlier.
- Prevention: validate inputs and use small samples.

- Failure: Expensive lineage recomputed.
- Symptom: repeated actions rerun full plan.
- Recovery: cache/persist/checkpoint.
- Prevention: cache reused expensive intermediate result.

## 12. Common Mistakes

- Mistake: Assuming no error means transformations succeeded.
- Why it is wrong: execution may not have happened yet.
- Better approach: remember action triggers real work.

- Mistake: Debugging with many `count()` calls.
- Why it is wrong: each count can be expensive.
- Better approach: use explain, sample, and Spark UI.

## 13. Mini Example

```python
plan = df.filter("country = 'US'").select("user_id")

# Nothing major has run yet.
plan.write.parquet("/output")

# Now the job runs.
```

## 14. Interview Questions

1. What is lazy evaluation?
2. Why does Spark use lazy evaluation?
3. What triggers execution?
4. Why can errors appear late?
5. How does `explain()` help?

## 15. Interview Speak

"Spark is lazy: transformations build a plan, and actions trigger execution. This allows Spark to optimize the full pipeline, push filters/projections, and schedule stages efficiently. The trade-off is delayed errors and possible recomputation if multiple actions reuse the same lineage."

## 16. Quick Recall

- One-line summary: Spark waits until an action to run the optimized plan.
- Three keywords: action, lineage, optimize.
- One trap: Thinking transformations have already run.
- One memory trick: Spark reads the whole recipe before cooking.
