# Topic 098: Adaptive Query Execution

## 1. Goal

Understand Adaptive Query Execution, or AQE, as Spark's ability to adjust query plans during runtime.

## 2. Baby Intuition

Before a trip, you choose a route.

During the trip, traffic changes, so GPS adjusts.

AQE is Spark's runtime GPS for query plans.

## 3. What It Is

- Simple definition: AQE lets Spark change parts of the plan while the job is running.
- Technical definition: Adaptive Query Execution dynamically optimizes Spark SQL physical plans at runtime using actual statistics from completed stages.
- Category: Runtime query optimization.
- Related terms: shuffle partition coalescing, skew join handling, join strategy conversion, runtime statistics.

## 4. Why It Exists

Before runtime, Spark estimates data sizes.

Estimates can be wrong.

AQE exists because actual runtime data can reveal:

- table is smaller than expected
- shuffle partitions are too many
- some partitions are skewed
- broadcast join is now possible

## 5. Where It Fits In A Data Platform

```text
Spark SQL/DataFrame plan -> runtime statistics -> AQE adjusts physical plan
```

AQE mainly helps Spark SQL/DataFrame workloads.

## 6. How It Works Step By Step

1. Spark creates initial physical plan.
2. Query starts running.
3. Shuffle stage completes and produces statistics.
4. Spark compares actual sizes with estimates.
5. Spark may adjust later stages.
6. New plan runs with better choices.

Common AQE features:

- coalesce small shuffle partitions
- handle skewed joins
- switch sort-merge join to broadcast join

## 7. How To Use It Practically

Enable/disable:

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
```

Common related configs:

```python
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

Inspect plan:

```python
df.explain(True)
```

Look for:

```text
AdaptiveSparkPlan
```

## 8. Real-World Scenario

- Product/system: Daily fact table join.
- Problem: Some days have much smaller input than expected.
- How AQE helps: Coalesces shuffle partitions or switches join strategy.
- What would go wrong without it: Job may use too many tiny tasks or inefficient join strategy.

## 9. System Design Angle

AQE helps reduce manual tuning, but it is not magic.

Still design for:

- good file layout
- sensible partitioning
- skew awareness
- correct join keys
- resource sizing

AQE improves runtime decisions; it does not fix bad data modeling.

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| runtime plan improvements | behavior can feel less predictable |
| fewer manual partition choices | requires shuffle statistics |
| skew handling | not all skew disappears |
| join strategy adaptation | still needs good configs |

## 11. Failure Modes

- Failure: AQE not enabled.
- Symptom: static poor plan.
- Recovery: enable if supported.
- Prevention: platform defaults/config review.

- Failure: AQE cannot fix extreme skew.
- Symptom: straggler tasks remain.
- Recovery: salting/custom skew handling.
- Prevention: data profiling.

## 12. Common Mistakes

- Mistake: Thinking AQE removes need for tuning.
- Why it is wrong: data layout, memory, and join logic still matter.
- Better approach: use AQE plus good design.

- Mistake: Not checking final adaptive plan.
- Why it is wrong: initial and final plans may differ.
- Better approach: inspect Spark UI/explain.

## 13. Mini Example

Initial plan:

```text
SortMergeJoin
```

Runtime discovers small side is tiny:

```text
BroadcastHashJoin
```

AQE may switch strategy.

## 14. Interview Questions

1. What is AQE?
2. What runtime optimizations can AQE do?
3. How does AQE help skew?
4. Does AQE replace tuning?
5. How do you know AQE is active?

## 15. Interview Speak

"Adaptive Query Execution lets Spark adjust physical query plans at runtime based on actual statistics. It can coalesce shuffle partitions, handle skew joins, and switch join strategies such as sort-merge to broadcast. It helps, but good data layout and tuning still matter."

## 16. Quick Recall

- One-line summary: AQE adjusts Spark SQL plans while running.
- Three keywords: adaptive, runtime, skew.
- One trap: Treating AQE as magic.
- One memory trick: AQE is Spark's GPS recalculating route.
