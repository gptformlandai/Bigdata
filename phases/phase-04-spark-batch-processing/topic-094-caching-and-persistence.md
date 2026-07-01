# Topic 094: Caching And Persistence

## 1. Goal

Understand when and how to cache data in Spark without wasting memory.

## 2. Baby Intuition

If you need to read the same chapter many times, keep the book open on your desk.

Spark cache keeps reused data closer so it does not recompute or reread it repeatedly.

## 3. What It Is

- Simple definition: Caching stores intermediate data for reuse.
- Technical definition: Spark caching/persistence stores partitions of an RDD/DataFrame in memory and/or disk so repeated actions can reuse computed results.
- Category: Performance optimization.
- Related terms: cache, persist, storage level, memory, disk, unpersist.

## 4. Why It Exists

Spark is lazy and may recompute lineage for repeated actions.

Caching helps when:

- same DataFrame is reused multiple times
- computation is expensive
- iterative algorithms need repeated access
- input source is slow

Without cache:

```text
same expensive transformations may run again and again
```

## 5. Where It Fits In A Data Platform

```text
Read -> expensive clean/join -> cache -> multiple downstream outputs
```

Common in:

- feature engineering
- iterative ML
- multiple reports from same cleaned dataset
- repeated interactive analysis

## 6. How It Works Step By Step

Code:

```python
clean = raw.filter("status is not null").select("user_id", "amount")
clean.cache()
```

Important:

```text
cache is lazy too
```

It materializes when an action runs:

```python
clean.count()
```

Then later actions can reuse cached partitions:

```python
clean.groupBy("user_id").sum("amount").show()
clean.groupBy("dt").count().show()
```

## 7. How To Use It Practically

Basic:

```python
df.cache()
```

Storage-level control:

```python
from pyspark import StorageLevel

df.persist(StorageLevel.MEMORY_AND_DISK)
```

Release cache:

```python
df.unpersist()
```

Inspect:

- Spark UI Storage tab
- cached partitions count
- memory used
- disk used

## 8. Real-World Scenario

- Product/system: Customer feature pipeline.
- Problem: Cleaned events dataset feeds 5 different feature outputs.
- How caching helps: Clean once, reuse multiple times.
- What would go wrong without it: Spark may repeat expensive cleaning and reads for each output.

## 9. System Design Angle

Cache when:

- data is reused
- recomputation is expensive
- cached data fits or spills acceptably

Do not cache when:

- data used once
- data is too huge
- memory is needed for joins/shuffles
- cache causes eviction and instability

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| faster repeated access | memory usage |
| avoids recomputation | eviction risk |
| useful for iterative jobs | cache materialization cost |
| can reduce source reads | stale cached data if source changes |

## 11. Failure Modes

- Failure: Cache too large.
- Symptom: eviction, spills, executor OOM.
- Recovery: unpersist, use disk storage, reduce data.
- Prevention: cache only reused columns/rows.

- Failure: Cache not materialized.
- Symptom: first later action still slow.
- Recovery: trigger action after cache if needed.
- Prevention: understand lazy cache.

- Failure: Forgetting unpersist.
- Symptom: memory pressure for later stages.
- Recovery: call `unpersist()`.
- Prevention: release no-longer-needed cached data.

## 12. Common Mistakes

- Mistake: Caching everything.
- Why it is wrong: memory is limited.
- Better approach: cache only expensive reused datasets.

- Mistake: Caching after a cheap read but before filter/select.
- Why it is wrong: stores too much data.
- Better approach: filter/select first, then cache smaller data.

## 13. Mini Example

```python
base = df.filter("dt = '2026-07-01'").select("user_id", "amount")
base.cache()
base.count()  # materialize

base.groupBy("user_id").sum("amount").write.parquet("/out1")
base.groupBy().avg("amount").write.parquet("/out2")

base.unpersist()
```

## 14. Interview Questions

1. What does cache do in Spark?
2. Cache vs persist?
3. Is cache eager or lazy?
4. When should you cache?
5. What problems can caching cause?

## 15. Interview Speak

"Caching stores intermediate partitions so reused DataFrames or RDDs do not need to be recomputed. It is useful for expensive data reused multiple times, but it consumes executor memory and can cause eviction or OOM if overused. Cache is lazy, so it materializes only after an action."

## 16. Quick Recall

- One-line summary: Cache reused expensive data, not everything.
- Three keywords: reuse, memory, unpersist.
- One trap: Cache is lazy.
- One memory trick: Keep the book open only if you will read it again.
