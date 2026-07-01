# Topic 090: Shuffle

## 1. Goal

Understand shuffle as the expensive data redistribution step in Spark.

## 2. Baby Intuition

Imagine every student has mixed cards.

To count cards by color, all red cards must go to one group, blue cards to another, and so on.

That movement is shuffle.

## 3. What It Is

- Simple definition: Shuffle is moving data across executors so related records land together.
- Technical definition: Spark shuffle redistributes data across partitions, typically by key, during wide transformations such as joins, groupBy, distinct, and repartition.
- Category: Distributed data movement.
- Related terms: shuffle read, shuffle write, spill, partition, exchange, wide transformation.

## 4. Why It Exists

Some operations need records with the same key to be together.

Examples:

- count orders per customer
- join orders with customers
- remove duplicates by id
- sort all rows globally

If matching records are on different machines, Spark must move data.

## 5. Where It Fits In A Data Platform

```text
Wide transformation -> Shuffle -> New partitions -> Next stage
```

Shuffle is often the most expensive part of Spark jobs.

## 6. How It Works Step By Step

For `groupBy("customer_id")`:

1. Each executor reads its input partition.
2. Spark computes target partition for each key.
3. Executor writes shuffle files.
4. Other executors fetch shuffle blocks.
5. Records with same key are grouped.
6. Reducer tasks aggregate values.

Spark UI shows:

- shuffle read
- shuffle write
- spill memory
- spill disk

## 7. How To Use It Practically

Operations that often shuffle:

```python
df.groupBy("customer_id").count()
df.join(other, "customer_id")
df.distinct()
df.orderBy("created_at")
df.repartition(200)
```

Config:

```python
spark.conf.set("spark.sql.shuffle.partitions", "200")
```

Default often may not match your data size. Tune based on workload.

## 8. Real-World Scenario

- Product/system: Daily customer revenue.
- Problem: Orders for the same customer are spread across files/partitions.
- How shuffle helps: Moves rows so each customer's orders can be aggregated together.
- What would go wrong without it: totals would be partial and incorrect.

## 9. System Design Angle

Shuffle affects:

- network cost
- disk I/O
- memory pressure
- runtime
- cloud cost

Reducing shuffle is a major Spark optimization skill.

Ways to reduce shuffle:

- filter early
- select fewer columns
- broadcast small table
- pre-aggregate
- avoid unnecessary `distinct`
- use correct partitioning
- handle skew

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| correct global grouping/joining | network movement |
| distributed aggregation | disk spill |
| repartitioned data | stage boundary |
| scalable joins | skew risk |

## 11. Failure Modes

- Failure: Shuffle spill to disk.
- Symptom: slow tasks and high disk I/O.
- Recovery: increase memory, reduce data, tune partitions.
- Prevention: filter/project early.

- Failure: Shuffle fetch failure.
- Symptom: task fails fetching shuffle block.
- Recovery: Spark retries or recomputes map output.
- Prevention: stable executors/network.

- Failure: Skewed shuffle.
- Symptom: one reducer task runs much longer.
- Recovery: salting, AQE skew handling, better keys.
- Prevention: inspect key distribution.

## 12. Common Mistakes

- Mistake: Calling `repartition` casually.
- Why it is wrong: it causes shuffle.
- Better approach: repartition only when needed.

- Mistake: Assuming `groupBy` is cheap.
- Why it is wrong: it usually shuffles data.
- Better approach: reduce input size first.

## 13. Mini Example

Before shuffle:

```text
partition 1: c1, c2
partition 2: c1, c3
```

After shuffle by customer:

```text
partition A: all c1 rows
partition B: c2 and c3 rows
```

## 14. Interview Questions

1. What is shuffle?
2. Which operations cause shuffle?
3. Why is shuffle expensive?
4. How do you reduce shuffle?
5. What is shuffle spill?

## 15. Interview Speak

"Shuffle is Spark's data redistribution step. It happens when records with the same key must be brought together, such as groupBy, join, distinct, orderBy, and repartition. Shuffle is expensive because it uses network, disk, and memory, so I reduce input data early and choose join/partitioning strategies carefully."

## 16. Quick Recall

- One-line summary: Shuffle moves data across executors by key.
- Three keywords: network, disk, key.
- One trap: Repartitioning without realizing it shuffles.
- One memory trick: Shuffle is everyone exchanging cards.
