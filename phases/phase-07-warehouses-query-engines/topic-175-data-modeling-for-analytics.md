# Topic 175: Data Modeling For Analytics

## 1. Goal

Understand how to design analytics tables that are understandable, correct, and fast.

## 2. Baby Intuition

Data modeling is arranging data so people can ask business questions without fighting the raw source systems.

It is like turning kitchen ingredients into a menu that customers can actually order from.

## 3. What It Is

- Simple definition: Data modeling for analytics is designing tables for reporting, BI, and analysis.
- Technical definition: Analytical data modeling defines facts, dimensions, grains, relationships, metric logic, history behavior, and aggregate structures to support reliable and performant analytical queries.
- Category: Warehouse/lakehouse modeling discipline.
- Related terms: star schema, fact, dimension, grain, metric, semantic layer, mart, SCD.

## 4. Why It Exists

Raw source data is not enough because:

- names are inconsistent
- schemas are operational, not analytical
- business logic is repeated in many queries
- metrics become inconsistent
- joins are confusing
- dashboards become slow

Modeling creates trusted tables that match business questions.

## 5. Where It Fits In A Data Platform

```text
raw/staging data
  -> cleaned intermediate models
  -> facts and dimensions
  -> marts/semantic layer
  -> dashboards, analysts, ML
```

## 6. How It Works Step By Step

1. Understand the business process.
2. Define the grain of each fact table.
3. Identify measures.
4. Identify dimensions.
5. Decide SCD/history behavior.
6. Build clean reusable models.
7. Create marts for teams/use cases.
8. Add quality tests and documentation.
9. Optimize physical layout and aggregates.

## 7. How To Use It Practically

Modeling checklist:

| Question | Why it matters |
|---|---|
| What does one row mean? | prevents double-counting |
| What metric is measured? | defines facts |
| What can users filter/group by? | defines dimensions |
| Does history matter? | defines SCD choice |
| Who owns the metric? | governance |
| How fresh must it be? | pipeline design |
| How often is it queried? | optimization |

## 8. Real-World Scenario

- Product/system: Company-wide revenue analytics.
- Problem: Sales, finance, and product teams calculate revenue differently.
- How modeling helps: create governed revenue facts, customer/product/date dimensions, and certified marts.
- What would go wrong without it: every team reports different numbers in leadership meetings.

## 9. System Design Angle

For analytics modeling, explain:

- ingestion layer
- staging/raw layer
- cleaned reusable layer
- facts/dimensions
- marts/semantic layer
- quality checks
- lineage and ownership
- performance optimizations

Example:

```text
orders_raw -> stg_orders -> fact_orders -> revenue_mart -> dashboard
```

## 10. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| raw flexible tables | easy ingestion | hard for business users |
| modeled marts | easy trusted analytics | modeling effort |
| star schema | simple BI joins | some denormalization |
| aggregates | fast dashboards | refresh/storage cost |
| Type 2 dimensions | historical accuracy | more complexity |

## 11. Failure Modes

- Failure: Undefined grain.
- Symptom: duplicated metrics.
- Recovery: redesign model.
- Prevention: document row meaning.

- Failure: Metric logic spread across dashboards.
- Symptom: inconsistent numbers.
- Recovery: centralize metric definitions.
- Prevention: semantic layer or certified marts.

- Failure: No data quality tests.
- Symptom: bad data silently reaches executives.
- Recovery: fix and backfill.
- Prevention: tests for uniqueness, nulls, ranges, relationships.

## 12. Common Mistakes

- Mistake: Copying OLTP schema directly into BI.
- Why it is wrong: operational schemas are not designed for easy analytics.
- Better approach: reshape into facts, dimensions, and marts.

- Mistake: Building dashboards directly on raw tables.
- Why it is wrong: repeated business logic becomes inconsistent and slow.
- Better approach: build governed models first.

- Mistake: Ignoring business definitions.
- Why it is wrong: correct SQL can still answer the wrong question.
- Better approach: align metrics with business owners.

## 13. Mini Example

```text
Business question:
What is monthly recurring revenue by customer segment?

Modeling decisions:
fact_subscription_revenue grain = one customer/month
dim_customer tracks segment history
metric definition = active paid subscription revenue
```

## 14. Interview Questions

1. How do you design an analytics model?
2. What is grain?
3. Why use facts and dimensions?
4. How do you prevent metric inconsistency?
5. How do quality tests fit into modeling?

## 15. Interview Speak

"For analytics modeling, I start from the business process and define the grain before choosing columns. Then I create facts for measurable events, dimensions for context, SCD handling for history, and marts or semantic models for trusted metrics. I add data quality tests, ownership, documentation, and performance optimizations like aggregates or clustering."

## 16. Quick Recall

- One-line summary: Analytics modeling turns raw data into trusted business questions.
- Three keywords: grain, metrics, marts.
- One trap: Correct SQL with wrong business definition.
- One memory trick: Raw ingredients need a menu.
