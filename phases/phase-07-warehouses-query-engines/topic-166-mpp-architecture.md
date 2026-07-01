# Topic 166: MPP Architecture

## 1. Goal

Understand massively parallel processing architecture in warehouses and analytical databases.

## 2. Baby Intuition

MPP is many workers splitting a huge SQL job.

Instead of one person counting every receipt, many workers count different piles and combine the totals.

## 3. What It Is

- Simple definition: MPP means many machines process one analytical query in parallel.
- Technical definition: Massively parallel processing is an architecture where data and query execution are distributed across multiple worker nodes that scan, join, aggregate, and exchange data in parallel.
- Category: Distributed analytical query architecture.
- Related terms: coordinator, worker, shard, partition, exchange, shuffle, distributed join, Redshift, Snowflake, BigQuery, Trino.

## 4. Why It Exists

Analytical datasets can be too large for one machine.

MPP improves:

- scan speed
- aggregation throughput
- parallel joins
- query concurrency
- scale-out capacity

One machine reading 100 TB is slow. Many machines reading parts of 100 TB is much faster.

## 5. Where It Fits In A Data Platform

```text
SQL query
  -> coordinator/planner
  -> many workers
  -> parallel scans/joins/aggregations
  -> final result
```

Used by warehouses and engines such as Redshift, Snowflake, BigQuery, Synapse, Trino, ClickHouse, Druid, and Pinot in different forms.

## 6. How It Works Step By Step

1. SQL is submitted.
2. Coordinator creates a distributed plan.
3. Data is split across workers or read in parallel.
4. Each worker scans its portion.
5. Workers filter and aggregate locally.
6. Data may be exchanged/shuffled for joins or global grouping.
7. Final results are merged and returned.

Example:

```text
Worker 1 scans January
Worker 2 scans February
Worker 3 scans March
Coordinator combines totals
```

## 7. How To Use It Practically

To help MPP systems:

- filter early
- select needed columns only
- avoid unnecessary huge shuffles
- choose good distribution keys where applicable
- pre-aggregate repeated queries
- model joins carefully
- monitor skew

## 8. Real-World Scenario

- Product/system: Sales warehouse.
- Problem: Query scans billions of sales rows by region/month.
- How MPP helps: workers scan partitions in parallel and combine aggregates.
- What would go wrong on one machine: scan and aggregation would take too long.

## 9. System Design Angle

Mention MPP when:

- query scans large datasets
- SQL needs distributed execution
- joins/aggregations are heavy
- warehouse scale-out matters
- data movement/skew is a concern

Key maturity:

```text
MPP speeds scans, but data movement can become the bottleneck.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| faster large scans | distributed complexity |
| scale-out compute | network shuffle cost |
| high throughput | skew can hurt |
| parallel aggregation | coordinator/planning overhead |
| supports big warehouses | poor data layout still hurts |

## 11. Failure Modes

- Failure: Data skew.
- Symptom: one worker runs much longer than others.
- Recovery: rebalance or change key.
- Prevention: choose distribution/partition keys carefully.

- Failure: Large shuffle.
- Symptom: network bottleneck and slow joins.
- Recovery: pre-aggregate, broadcast small table, colocate data.
- Prevention: model joins and distribution.

- Failure: Too many tiny files/splits.
- Symptom: scheduling overhead.
- Recovery: compaction.
- Prevention: control file sizes.

## 12. Common Mistakes

- Mistake: Thinking more workers always means faster.
- Why it is wrong: bottlenecks can be shuffle, skew, or planning.
- Better approach: identify the real bottleneck.

- Mistake: Ignoring data distribution.
- Why it is wrong: poor distribution causes network-heavy joins.
- Better approach: design around common join/filter patterns.

## 13. Mini Example

```text
COUNT orders by country:

Each worker:
  counts local rows by country

Final stage:
  merges worker counts into global totals
```

## 14. Interview Questions

1. What is MPP?
2. Why is MPP useful for warehouses?
3. What is a distributed join?
4. How does skew hurt MPP?
5. Why can data movement dominate?

## 15. Interview Speak

"MPP architectures split analytical SQL work across many workers. Each worker scans and processes part of the data, then exchanges or merges intermediate results. This is powerful for large scans and aggregations, but performance depends on partitioning, distribution, skew, and network movement."

## 16. Quick Recall

- One-line summary: MPP means many workers execute one analytical query in parallel.
- Three keywords: workers, exchange, skew.
- One trap: More workers cannot fix bad shuffles.
- One memory trick: Many people count separate piles.
