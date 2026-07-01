# Topic 091: Broadcast Join

## 1. Goal

Understand broadcast join as a way to avoid shuffling a large table when joining with a small table.

## 2. Baby Intuition

Imagine many workers each have a huge pile of orders.

They all need a tiny lookup table of country codes.

Instead of moving all orders to one place, give every worker a copy of the tiny lookup table.

That is broadcast join.

## 3. What It Is

- Simple definition: Broadcast join sends a small table to every executor so a large table can join locally.
- Technical definition: Broadcast hash join replicates a small relation to all executors and builds an in-memory hash table for local joins with partitions of a larger relation.
- Category: Spark join optimization.
- Related terms: broadcast variable, hash join, small dimension table, shuffle avoidance.

## 4. Why It Exists

Normal joins can shuffle both tables by join key.

If one table is small, shuffling the huge table is wasteful.

Broadcast join exists to avoid expensive shuffle when one side fits in executor memory.

## 5. Where It Fits In A Data Platform

```text
large fact table + small dimension table -> broadcast join -> enriched result
```

Common in:

- orders + country lookup
- clicks + campaign metadata
- transactions + risk rules
- events + small configuration table

## 6. How It Works Step By Step

1. Spark identifies small table.
2. Driver/executors collect and broadcast small table to executors.
3. Each executor builds a hash map in memory.
4. Large table partitions stay distributed.
5. Each executor joins its local large rows with broadcasted small table.
6. No large-table shuffle is needed.

## 7. How To Use It Practically

Automatic broadcast can happen based on size.

Manual hint:

```python
from pyspark.sql.functions import broadcast

result = large_orders.join(
    broadcast(country_lookup),
    "country_code",
    "left"
)
```

Config:

```python
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 10485760)
```

This example threshold is 10 MB.

## 8. Real-World Scenario

- Product/system: Clickstream enrichment.
- Problem: Add campaign attributes to billions of click events.
- How broadcast join helps: Campaign table is small and can be copied to executors.
- What would go wrong without it: Spark may shuffle huge clickstream data.

## 9. System Design Angle

Use broadcast join when:

- one table is small enough
- executor memory can hold it
- join is repeated across large partitions
- avoiding shuffle is valuable

Avoid when:

- "small" table is not actually small
- table expands after filters
- executor memory is tight
- many broadcasts happen at once

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| avoids large shuffle | memory used on every executor |
| faster joins | broadcast timeout risk |
| simple dimension enrichment | not good for large tables |
| less network for fact table | driver/executor pressure |

## 11. Failure Modes

- Failure: Broadcast table too large.
- Symptom: executor OOM or broadcast timeout.
- Recovery: disable broadcast or increase resources.
- Prevention: check size and filter small side.

- Failure: Wrong join side broadcast.
- Symptom: huge memory use.
- Recovery: remove hint or hint correct table.
- Prevention: understand table sizes.

## 12. Common Mistakes

- Mistake: Broadcasting a table because it has few columns.
- Why it is wrong: row count/bytes matter, not only columns.
- Better approach: check actual size.

- Mistake: Broadcasting multiple medium tables.
- Why it is wrong: executor memory can fill.
- Better approach: broadcast only truly small dimensions.

## 13. Mini Example

```text
Large table: 1 TB clicks
Small table: 5 MB country codes

Broadcast 5 MB to executors.
Do local joins against click partitions.
```

## 14. Interview Questions

1. What is broadcast join?
2. When should you use it?
3. How does it reduce shuffle?
4. What can go wrong with broadcast join?
5. How do you force broadcast in PySpark?

## 15. Interview Speak

"A broadcast join copies a small table to every executor so each partition of a large table can join locally. It avoids shuffling the large table and is useful for joining fact data with small dimension tables. The risk is executor memory pressure if the broadcast side is too large."

## 16. Quick Recall

- One-line summary: Broadcast small table to avoid big shuffle.
- Three keywords: small, local, memory.
- One trap: Broadcasting a table that is not actually small.
- One memory trick: Give every worker the tiny lookup sheet.
