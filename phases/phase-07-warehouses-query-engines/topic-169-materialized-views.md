# Topic 169: Materialized Views

## 1. Goal

Understand materialized views as precomputed query results stored for faster reads.

## 2. Baby Intuition

A normal view is like a recipe.

A materialized view is like cooked food already prepared and stored.

## 3. What It Is

- Simple definition: A materialized view stores the result of a query.
- Technical definition: A materialized view is a persisted, precomputed query result that can be refreshed and used to speed up repeated expensive queries.
- Category: Query acceleration and precomputation.
- Related terms: view, refresh, incremental refresh, aggregate table, cache, query rewrite.

## 4. Why It Exists

Some queries are expensive and repeated:

- daily revenue by region
- active users by day
- sales by product category
- fraud alerts by hour

Instead of recomputing from raw facts every time, materialized views store the answer or partial answer.

## 5. Where It Fits In A Data Platform

```text
raw/detail table
  -> materialized view / aggregate table
  -> dashboard queries
```

Materialized views often serve BI dashboards and repeated analytics.

## 6. How It Works Step By Step

1. Define a query.
2. Engine computes the query result.
3. Result is stored physically.
4. Users query the materialized view directly or optimizer rewrites queries to use it.
5. View is refreshed on schedule or incrementally.
6. Dashboard reads become faster.

## 7. How To Use It Practically

Example:

```sql
CREATE MATERIALIZED VIEW daily_sales AS
SELECT order_date, region, SUM(amount) AS revenue
FROM fact_orders
GROUP BY order_date, region;
```

Use when:

- query is repeated often
- query is expensive
- freshness can be slightly delayed
- result size is much smaller than raw data

## 8. Real-World Scenario

- Product/system: Executive sales dashboard.
- Problem: Dashboard repeatedly scans billions of order rows.
- How materialized view helps: precompute revenue by day/region so dashboard reads small aggregated data.
- What would go wrong without it: every dashboard load repeats the same expensive group-by.

## 9. System Design Angle

Clarify:

- freshness requirement
- refresh frequency
- full vs incremental refresh
- storage cost
- query rewrite support
- failure handling

Design pattern:

```text
fact_events -> daily aggregate materialized view -> dashboard
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| faster repeated queries | extra storage |
| lower compute for dashboards | refresh complexity |
| predictable latency | stale results possible |
| reduces raw scans | must handle refresh failures |

## 11. Failure Modes

- Failure: Refresh fails.
- Symptom: dashboard shows stale data.
- Recovery: rerun refresh and alert users if needed.
- Prevention: monitor freshness.

- Failure: View no longer matches business logic.
- Symptom: wrong metric definitions.
- Recovery: update view and backfill.
- Prevention: data contract and review.

- Failure: Too many materialized views.
- Symptom: high storage/refresh cost.
- Recovery: remove unused views.
- Prevention: usage monitoring.

## 12. Common Mistakes

- Mistake: Materializing every query.
- Why it is wrong: storage and refresh cost explode.
- Better approach: materialize repeated expensive queries.

- Mistake: Ignoring staleness.
- Why it is wrong: users may assume results are current.
- Better approach: show/monitor freshness SLA.

## 13. Mini Example

```text
Raw table:
10 billion order rows

Materialized view:
365 days x 20 regions = 7,300 rows

Dashboard reads 7,300 rows instead of 10 billion.
```

## 14. Interview Questions

1. What is a materialized view?
2. How is it different from a normal view?
3. When should you use one?
4. What is refresh cost?
5. How can staleness hurt?

## 15. Interview Speak

"A materialized view stores a precomputed query result. I would use it for repeated expensive dashboard queries where the result is much smaller than the raw data and a known freshness SLA is acceptable. The trade-offs are storage, refresh cost, and staleness."

## 16. Quick Recall

- One-line summary: Materialized views store expensive answers ahead of time.
- Three keywords: precompute, refresh, staleness.
- One trap: Materializing everything.
- One memory trick: Cooked food, not just recipe.
