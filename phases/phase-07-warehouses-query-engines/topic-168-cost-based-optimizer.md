# Topic 168: Cost-Based Optimizer

## 1. Goal

Understand how a cost-based optimizer chooses efficient query plans.

## 2. Baby Intuition

A cost-based optimizer is like a route planner.

It estimates different routes and picks the one expected to be cheapest.

## 3. What It Is

- Simple definition: A cost-based optimizer chooses a query plan using estimated costs.
- Technical definition: A cost-based optimizer uses table statistics, cardinality estimates, data sizes, selectivity, and operator costs to compare alternative physical query plans.
- Category: Query optimization.
- Related terms: statistics, cardinality, selectivity, join order, cost model, histogram, EXPLAIN.

## 4. Why It Exists

The same SQL can run many ways:

- join A then B
- join B then C
- broadcast small table
- shuffle both tables
- use hash join
- use sort-merge join
- scan partitioned data first

Some plans are much cheaper than others.

The optimizer exists to pick a good plan automatically.

## 5. Where It Fits In A Data Platform

```text
SQL query
  -> logical plan
  -> optimizer estimates plan alternatives
  -> lowest-cost physical plan
  -> execution
```

Used in warehouses, Spark SQL, Trino, PostgreSQL, BigQuery, Snowflake, Redshift, and many query engines.

## 6. How It Works Step By Step

1. Read query structure.
2. Read table and column statistics.
3. Estimate how many rows each filter returns.
4. Estimate join output sizes.
5. Compare possible join orders and algorithms.
6. Estimate CPU, I/O, memory, and network cost.
7. Choose the lowest estimated cost plan.
8. Execute the plan.

## 7. How To Use It Practically

Help the optimizer by:

- keeping statistics fresh
- avoiding overly complex expressions that block pushdown
- using clear join conditions
- filtering early in SQL
- designing tables for common joins
- avoiding unnecessary casts on filter columns
- using partitioning/clustering well

Common maintenance idea:

```sql
ANALYZE table_name;
```

Exact syntax differs by engine.

## 8. Real-World Scenario

- Product/system: Customer revenue mart.
- Problem: Query joins a huge orders table to a small customer segment table.
- How CBO helps: chooses to broadcast the small table instead of shuffling both huge datasets.
- What would go wrong with bad stats: optimizer may treat the small table as large and choose a slow shuffle plan.

## 9. System Design Angle

Mention CBO when:

- query planner choices matter
- join order is important
- table statistics are stale
- skew/cardinality estimates are wrong
- query plans differ between environments

Strong phrase:

```text
The optimizer is only as good as its metadata and statistics.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| automatic plan improvement | estimates can be wrong |
| better join ordering | requires stats maintenance |
| reduces manual hints | complex to debug |
| adapts to data sizes | can change plans unexpectedly |

## 11. Failure Modes

- Failure: Stale table stats.
- Symptom: wrong join order or memory blowup.
- Recovery: refresh stats.
- Prevention: stats maintenance after large loads.

- Failure: Data skew hidden by averages.
- Symptom: one worker slow.
- Recovery: skew-aware rewrite.
- Prevention: inspect key distribution.

- Failure: Predicate selectivity misestimated.
- Symptom: optimizer chooses bad scan/join strategy.
- Recovery: rewrite query or update stats/histograms.
- Prevention: collect useful column stats.

## 12. Common Mistakes

- Mistake: Believing optimizer always picks the best plan.
- Why it is wrong: it picks the best plan based on estimates, which can be wrong.
- Better approach: inspect plans and maintain stats.

- Mistake: Ignoring casts/functions on filter columns.
- Why it is wrong: they may prevent pruning or stats use.
- Better approach: keep predicates simple and type-aligned.

## 13. Mini Example

```text
Join orders (1 billion rows) with countries (250 rows).

Good plan:
broadcast countries to all workers.

Bad plan:
shuffle both tables across network.
```

## 14. Interview Questions

1. What is a cost-based optimizer?
2. What statistics does it use?
3. Why can stale stats hurt?
4. How does CBO choose join order?
5. What is cardinality estimation?

## 15. Interview Speak

"A cost-based optimizer compares possible query plans using statistics such as row counts, data size, selectivity, and cardinality. It chooses the estimated cheapest plan, but stale stats, skew, or bad predicates can cause poor choices, so I would inspect EXPLAIN and maintain statistics."

## 16. Quick Recall

- One-line summary: CBO picks the cheapest estimated query plan.
- Three keywords: stats, cardinality, join order.
- One trap: Trusting bad estimates.
- One memory trick: Query route planner.
