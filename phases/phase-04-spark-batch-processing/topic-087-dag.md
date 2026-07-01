# Topic 087: DAG

## 1. Goal

Understand DAG as Spark's execution graph of operations.

## 2. Baby Intuition

A DAG is like a flowchart with no loops going backward.

Spark uses it to understand:

```text
read data -> filter -> join -> aggregate -> write
```

## 3. What It Is

- Simple definition: A DAG is Spark's graph of computation steps.
- Technical definition: DAG stands for Directed Acyclic Graph, a directed graph of transformations where dependencies flow forward without cycles.
- Category: Execution planning concept.
- Related terms: lineage, stage, task, dependency, transformation.

## 4. Why It Exists

Spark needs to know how transformations depend on each other.

The DAG helps Spark:

- optimize operations
- split work into stages
- understand failure recovery
- know what must run before what
- avoid unnecessary work

## 5. Where It Fits In A Data Platform

```text
Spark code -> DAG -> stages -> tasks -> cluster execution
```

Every Spark job has a DAG behind it.

## 6. How It Works Step By Step

Code:

```python
result = (
    orders
    .filter("status = 'paid'")
    .join(customers, "customer_id")
    .groupBy("region")
    .sum("amount")
)
```

DAG idea:

```text
orders scan
  -> filter paid
  -> join customers
  -> group by region
  -> write result
```

Wide operations like join/groupBy create stage boundaries because they require shuffle.

## 7. How To Use It Practically

Look at:

- Spark UI DAG visualization
- SQL physical plan
- Jobs and stages

Command:

```python
result.explain(True)
```

For RDDs:

```python
rdd.toDebugString()
```

## 8. Real-World Scenario

- Product/system: Fraud analytics ETL.
- Problem: Join transactions with user profiles and aggregate risk metrics.
- How DAG helps: Spark understands dependencies and can schedule tasks safely.
- What would go wrong without it: Spark could not optimize or recover lost partitions cleanly.

## 9. System Design Angle

DAG matters when explaining:

- why Spark can optimize multi-step jobs
- how fault recovery works through lineage
- why shuffle creates stage boundaries
- why one action creates one or more jobs

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| clear dependency tracking | complex plans can be hard to read |
| fault recovery through lineage | long lineage can be expensive |
| stage planning | shuffle boundaries still costly |

## 11. Failure Modes

- Failure: Very long lineage.
- Symptom: recomputation after failure is expensive.
- Recovery: checkpoint.
- Prevention: checkpoint iterative/long jobs.

- Failure: DAG contains huge shuffle.
- Symptom: slow stage and spilled data.
- Recovery: optimize joins/aggregations.
- Prevention: understand wide dependencies.

## 12. Common Mistakes

- Mistake: Thinking DAG is only a UI picture.
- Why it is wrong: DAG is Spark's real dependency model.
- Better approach: connect DAG to stages and recovery.

- Mistake: Ignoring stage boundaries.
- Why it is wrong: boundaries often mean shuffle and cost.
- Better approach: inspect stages in Spark UI.

## 13. Mini Example

```text
A -> B -> C
 \
  -> D -> E
```

Arrows mean dependency. Spark cannot run a dependent step before its parent data exists.

## 14. Interview Questions

1. What is a DAG?
2. Why does Spark build a DAG?
3. How does DAG help failure recovery?
4. What creates stage boundaries?
5. DAG vs stage?

## 15. Interview Speak

"Spark represents transformations as a DAG, a directed acyclic graph of dependencies. The DAG lets Spark optimize execution, split work into stages, schedule tasks, and recompute lost data through lineage. Shuffle operations usually create stage boundaries."

## 16. Quick Recall

- One-line summary: DAG is Spark's dependency graph.
- Three keywords: directed, acyclic, lineage.
- One trap: Not connecting DAG to stages.
- One memory trick: DAG is Spark's flowchart.
