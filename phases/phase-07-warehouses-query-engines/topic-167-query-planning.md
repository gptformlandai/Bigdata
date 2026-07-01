# Topic 167: Query Planning

## 1. Goal

Understand how a SQL engine turns a query into executable steps.

## 2. Baby Intuition

SQL says what you want.

Query planning decides how to get it.

It is like saying "bring dinner" versus planning the shopping, cooking, timing, and serving steps.

## 3. What It Is

- Simple definition: Query planning converts SQL into an execution plan.
- Technical definition: Query planning parses, validates, optimizes, and transforms a SQL query into physical operations such as scans, filters, joins, aggregations, exchanges, and sorts.
- Category: Query engine internals.
- Related terms: parser, logical plan, physical plan, optimizer, execution plan, scan, join, aggregation.

## 4. Why It Exists

SQL is declarative:

```sql
SELECT region, SUM(amount)
FROM orders
JOIN customers USING (customer_id)
GROUP BY region;
```

The query does not say:

- which table to scan first
- whether to filter before join
- which join algorithm to use
- how many workers to use
- whether to broadcast a small table
- which partitions/files to skip

The planner decides these details.

## 5. Where It Fits In A Data Platform

```text
SQL text
  -> parse
  -> analyze/validate
  -> logical plan
  -> optimized logical plan
  -> physical plan
  -> distributed execution
```

Every warehouse/query engine has some version of this process.

## 6. How It Works Step By Step

1. Parse SQL into a syntax tree.
2. Validate table names, columns, functions, and permissions.
3. Build a logical plan.
4. Apply optimizations like predicate pushdown and projection pruning.
5. Choose physical operators like hash join or sort-merge join.
6. Split work across workers if distributed.
7. Execute the plan.
8. Return results.

## 7. How To Use It Practically

You inspect query plans to understand:

- full table scans
- missing partition pruning
- join order
- broadcast vs shuffle joins
- expensive sorts
- spilled memory
- repeated subqueries
- data movement

Typical command names differ by engine, but the idea is:

```sql
EXPLAIN SELECT ...
```

## 8. Real-World Scenario

- Product/system: Revenue dashboard query.
- Problem: Query became slow after joining a new customer table.
- How planning helps: EXPLAIN reveals a huge shuffle join because stats are stale or join order is poor.
- What would go wrong without it: team guesses blindly and only increases compute.

## 9. System Design Angle

Mention query planning when:

- SQL is slow
- joins are heavy
- partition pruning matters
- data skipping matters
- engine behavior needs explanation

Good maturity:

```text
I would inspect the execution plan before tuning blindly.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| can find bottlenecks | plans can be complex |
| enables optimizer improvements | estimates may be wrong |
| avoids blind tuning | engine-specific details |
| shows scans and joins | plan changes across versions |

## 11. Failure Modes

- Failure: Bad statistics.
- Symptom: optimizer chooses poor join order.
- Recovery: refresh/analyze stats.
- Prevention: stats maintenance.

- Failure: Predicate not pushed down.
- Symptom: too much data scanned.
- Recovery: rewrite query or use better connector.
- Prevention: test common query patterns.

- Failure: Huge shuffle.
- Symptom: network/memory bottleneck.
- Recovery: pre-aggregate, broadcast small dimension, redesign layout.
- Prevention: model data for joins.

## 12. Common Mistakes

- Mistake: Looking only at final query duration.
- Why it is wrong: duration does not show where time was spent.
- Better approach: inspect plan, scanned bytes, shuffle, and spill.

- Mistake: Assuming SQL text order is execution order.
- Why it is wrong: optimizer may reorder operations.
- Better approach: read the logical/physical plan.

## 13. Mini Example

```text
SQL:
SELECT SUM(amount)
FROM orders
WHERE order_date = '2026-07-01';

Good plan:
prune date partition -> scan amount column -> aggregate

Bad plan:
scan all dates -> filter later -> aggregate
```

## 14. Interview Questions

1. What is query planning?
2. Logical plan vs physical plan?
3. What is predicate pushdown?
4. Why inspect EXPLAIN?
5. How can stale stats hurt a query?

## 15. Interview Speak

"Query planning is the process of turning declarative SQL into executable operations. I would inspect the plan to see scans, filters, joins, exchanges, pruning, and aggregation. For slow analytics queries, EXPLAIN is often the first serious debugging tool."

## 16. Quick Recall

- One-line summary: Query planning decides how SQL will run.
- Three keywords: logical plan, physical plan, EXPLAIN.
- One trap: Tuning without reading the plan.
- One memory trick: SQL says what; planner decides how.
