# Topic 089: Narrow Vs Wide Transformations

## 1. Goal

Understand why some Spark transformations are cheap and local while others require expensive data movement.

## 2. Baby Intuition

Narrow transformation:

```text
Each worker can finish using its own data.
```

Wide transformation:

```text
Workers must exchange data with each other.
```

That exchange is usually shuffle.

## 3. What It Is

- Simple definition: Narrow transformations do not require data movement across partitions; wide transformations do.
- Technical definition: A narrow dependency means each child partition depends on a small number of parent partitions, while a wide dependency means data must be redistributed across partitions, often through shuffle.
- Category: Spark execution dependency.
- Related terms: shuffle, stage boundary, partition, dependency.

## 4. Why It Exists

Spark needs to know whether data can be processed locally or must move across the network.

This matters because:

- local work is faster
- network shuffle is expensive
- shuffle creates stage boundaries
- wide transformations are common bottlenecks

## 5. Where It Fits In A Data Platform

```text
DataFrame operations -> narrow/wide dependencies -> stages/shuffle
```

This is central to ETL performance.

## 6. How It Works Step By Step

Narrow example:

```python
df.filter("amount > 100")
df.select("customer_id", "amount")
```

Each partition can filter/select independently.

Wide example:

```python
df.groupBy("customer_id").count()
df.join(other, "customer_id")
df.orderBy("amount")
```

Data with same key may live in different partitions, so Spark redistributes it.

## 7. How To Use It Practically

Common narrow transformations:

- `select`
- `filter`
- `withColumn`
- `map` when no repartition
- `union` in many cases

Common wide transformations:

- `groupBy`
- `join`
- `distinct`
- `dropDuplicates`
- `orderBy`
- `repartition`

Production habit:

```text
Before a groupBy/join/distinct, ask: how big is the shuffle?
```

## 8. Real-World Scenario

- Product/system: Customer spend aggregation.
- Problem: Need total spend per customer.
- Why wide transformation occurs: all rows for the same customer must meet in the same reducer partition.
- What would go wrong without shuffle: partial counts would be split across executors.

## 9. System Design Angle

Wide transformations affect:

- network
- disk spill
- memory
- runtime
- cost
- stage count

Optimization approach:

- filter early
- select needed columns
- pre-aggregate
- broadcast small tables
- avoid unnecessary distinct/orderBy

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| narrow ops are fast/local | limited operation types |
| wide ops enable joins/aggregations | shuffle cost |
| correct global grouping | network and disk spill |

## 11. Failure Modes

- Failure: Large wide transformation.
- Symptom: slow shuffle stage.
- Recovery: tune partitions and reduce data.
- Prevention: filter/project early.

- Failure: Skewed wide key.
- Symptom: one task huge.
- Recovery: salting or skew handling.
- Prevention: inspect key distribution.

## 12. Common Mistakes

- Mistake: Treating all transformations equally.
- Why it is wrong: wide transformations are much more expensive.
- Better approach: identify shuffle operations.

- Mistake: Sorting full dataset unnecessarily.
- Why it is wrong: global sort is expensive.
- Better approach: sort only when required.

## 13. Mini Example

```text
filter:
partition 1 -> partition 1 result

groupBy:
partition 1,2,3 -> shuffle by key -> new partitions
```

## 14. Interview Questions

1. What is a narrow transformation?
2. What is a wide transformation?
3. Why does groupBy require shuffle?
4. Give examples of narrow and wide operations.
5. Why are wide transformations expensive?

## 15. Interview Speak

"Narrow transformations can be computed within each partition, like filter or select. Wide transformations require data redistribution across partitions, like groupBy, join, distinct, or orderBy. Wide transformations cause shuffle, which is often the biggest Spark performance cost."

## 16. Quick Recall

- One-line summary: Narrow stays local; wide moves data.
- Three keywords: local, shuffle, stage.
- One trap: Forgetting joins/groupBy cause shuffle.
- One memory trick: Narrow is same table; wide is everyone swaps seats.
