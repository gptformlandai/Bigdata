# Topic 092: Sort-Merge Join

## 1. Goal

Understand sort-merge join as Spark's common strategy for joining large tables.

## 2. Baby Intuition

If two huge lists are too large to copy everywhere, sort both lists by the join key.

Then walk through them in order and match keys.

That is the idea behind sort-merge join.

## 3. What It Is

- Simple definition: Sort-merge join joins large tables by shuffling and sorting both sides by key.
- Technical definition: Sort-merge join repartitions both input relations by join key, sorts records within partitions, and merges matching sorted streams.
- Category: Spark join algorithm.
- Related terms: shuffle, sort, join key, partition, large table join.

## 4. Why It Exists

Broadcast join works only when one side is small.

When both tables are large:

```text
large table + large table
```

Spark often uses sort-merge join because it scales across partitions.

## 5. Where It Fits In A Data Platform

Common examples:

- orders join transactions
- clicks join impressions
- user events join user sessions
- CDC records join historical table

## 6. How It Works Step By Step

For join on `customer_id`:

1. Spark shuffles left table by `customer_id`.
2. Spark shuffles right table by `customer_id`.
3. Matching keys land in same partitions.
4. Spark sorts each partition by key.
5. Spark scans both sorted sides and matches rows.
6. Joined result is emitted.

## 7. How To Use It Practically

Code:

```python
joined = orders.join(payments, "order_id")
```

Spark may choose sort-merge join when:

- both sides are large
- broadcast is not possible
- join keys are sortable

Inspect:

```python
joined.explain(True)
```

Look for:

```text
SortMergeJoin
Exchange
Sort
```

## 8. Real-World Scenario

- Product/system: Finance reconciliation.
- Problem: Join large orders table with large payments table.
- How sort-merge join helps: Scales join across cluster when neither side can be broadcast.
- What would go wrong without it: Single-machine join would not fit, and broadcast would OOM.

## 9. System Design Angle

Sort-merge join is robust for large joins, but expensive.

Cost comes from:

- shuffling both sides
- sorting data
- possible spill to disk
- skewed join keys

Optimization:

- filter early
- select needed columns
- broadcast if one side becomes small
- bucket/partition data by join key when useful
- enable AQE
- fix skew

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| scalable large-table joins | shuffle both sides |
| memory safer than huge broadcast | sorting cost |
| works for big datasets | skew can hurt badly |
| predictable strategy | may spill to disk |

## 11. Failure Modes

- Failure: Join key skew.
- Symptom: one task handles huge key.
- Recovery: salting, AQE skew join, split hot key.
- Prevention: profile key distribution.

- Failure: Sort spill.
- Symptom: slow task, disk spill metrics.
- Recovery: tune memory/partitions.
- Prevention: reduce input size.

## 12. Common Mistakes

- Mistake: Joining wide tables with unnecessary columns.
- Why it is wrong: more data shuffles.
- Better approach: select only needed columns before join.

- Mistake: Assuming large joins are cheap because Spark is distributed.
- Why it is wrong: distributed shuffle/sort can be expensive.
- Better approach: estimate data size and join strategy.

## 13. Mini Example

```text
Left by key:  A, A, B, C
Right by key: A, B, B, D

Merge sorted streams:
A joins A
B joins B,B
C no match
```

## 14. Interview Questions

1. What is sort-merge join?
2. When does Spark use it?
3. Why does it require shuffle?
4. Broadcast join vs sort-merge join?
5. How do you optimize large joins?

## 15. Interview Speak

"Sort-merge join is Spark's common strategy for large joins when neither side is small enough to broadcast. Spark shuffles both sides by join key, sorts each partition, and merges matching keys. It scales, but shuffle, sort, spill, and skew can make it expensive."

## 16. Quick Recall

- One-line summary: Sort both large sides by key, then merge.
- Three keywords: shuffle, sort, merge.
- One trap: Not selecting columns before join.
- One memory trick: Two sorted phone books matched by name.
