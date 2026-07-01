# Topic 102: Spark Performance Tuning

## 1. Goal

Learn a practical tuning checklist for slow Spark jobs.

## 2. Baby Intuition

Tuning Spark is like fixing traffic.

You need to know whether the problem is:

- too many cars
- bad roads
- one blocked lane
- poor route
- not enough workers

In Spark terms: data size, shuffle, skew, files, memory, partitions, joins.

## 3. What It Is

- Simple definition: Spark tuning means improving job speed, cost, and reliability.
- Technical definition: Spark performance tuning is the process of optimizing data layout, query plans, partitions, joins, memory, caching, resource allocation, and failure behavior.
- Category: Production optimization.
- Related terms: Spark UI, shuffle, skew, partitioning, caching, AQE, file format.

## 4. Why It Exists

Spark can process huge data, but bad jobs can be slow and expensive.

Common causes:

- scanning too much data
- too many small files
- poor partitioning
- huge shuffle
- data skew
- wrong join strategy
- bad memory settings
- overuse of UDFs
- unnecessary actions

## 5. Where It Fits In A Data Platform

```text
Spark job -> observe metrics -> identify bottleneck -> tune -> verify
```

Tuning is part of operating production pipelines.

## 6. How It Works Step By Step

Basic tuning workflow:

1. Check Spark UI.
2. Identify slow job/stage.
3. Check if stage has shuffle.
4. Compare task durations and input sizes.
5. Look for skew/stragglers.
6. Check spill and GC.
7. Inspect physical plan.
8. Optimize query/data layout/config.
9. Rerun and compare.

## 7. How To Use It Practically

Tuning checklist:

- Use Parquet/ORC instead of CSV/JSON for analytics.
- Filter early.
- Select only needed columns.
- Avoid unnecessary `distinct` and `orderBy`.
- Broadcast small tables.
- Tune `spark.sql.shuffle.partitions`.
- Enable AQE.
- Fix skew.
- Compact small files.
- Cache only reused expensive data.
- Avoid `collect()` and large `toPandas()`.
- Prefer built-in functions over UDFs.

## 8. Real-World Scenario

- Product/system: Daily lakehouse ETL.
- Problem: Job takes 4 hours and misses SLA.
- Tuning path: Spark UI shows one join stage with huge shuffle and skew.
- Fix: filter earlier, broadcast dimension table, salt hot key, enable AQE, compact output.
- Result: lower runtime and cost.

## 9. System Design Angle

Performance tuning affects:

- SLA
- cluster size
- cloud cost
- downstream freshness
- reliability

Interview framing:

```text
I first measure, then optimize the bottleneck.
```

Do not randomly change configs.

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| faster jobs | tuning time |
| lower cost | more complexity |
| fewer failures | need observability |
| better SLA | optimizations can be workload-specific |

## 11. Failure Modes

- Failure: Tuning blindly.
- Symptom: no improvement or worse performance.
- Recovery: return to metrics and isolate bottleneck.
- Prevention: use Spark UI and explain plans.

- Failure: Over-caching.
- Symptom: memory pressure and eviction.
- Recovery: unpersist.
- Prevention: cache selectively.

- Failure: Over-partitioning.
- Symptom: many tiny tasks/files.
- Recovery: reduce partition count.
- Prevention: choose partition counts based on data size.

## 12. Common Mistakes

- Mistake: Starting with executor config before query/data layout.
- Why it is wrong: data layout/shuffle often dominates.
- Better approach: inspect plan and stage metrics first.

- Mistake: Assuming more executors always makes jobs faster.
- Why it is wrong: bottleneck may be skew, small files, or shuffle.
- Better approach: identify actual bottleneck.

## 13. Mini Example

Slow job diagnosis:

```text
Spark UI:
Stage 8 takes 90 minutes.
One task takes 88 minutes.
Shuffle read huge for one task.

Likely issue:
data skew.
```

## 14. Interview Questions

1. How do you tune a slow Spark job?
2. What do you check in Spark UI?
3. How do you reduce shuffle?
4. How do you handle skew?
5. Why can more executors fail to help?

## 15. Interview Speak

"I tune Spark by measuring first. I inspect Spark UI and physical plans to identify whether the bottleneck is scan size, shuffle, skew, spill, memory, file layout, or join strategy. Then I apply targeted fixes like filtering early, column pruning, broadcast joins, partition tuning, AQE, skew handling, compaction, and selective caching."

## 16. Quick Recall

- One-line summary: Measure first, then tune the real bottleneck.
- Three keywords: Spark UI, shuffle, skew.
- One trap: Random config tuning.
- One memory trick: Diagnose traffic before widening roads.
