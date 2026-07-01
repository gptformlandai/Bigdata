# Topic 156: Snowflake

## 1. Goal

Understand Snowflake as a cloud data warehouse and why teams use it for analytics.

## 2. Baby Intuition

Snowflake is like a managed analytics building where storage rooms and worker teams are separate.

Your data sits in storage, and you can start different compute warehouses to query it.

## 3. What It Is

- Simple definition: Snowflake is a managed cloud data warehouse platform.
- Technical definition: Snowflake separates storage, compute, and cloud services so users can store analytical data and query it with independently scalable virtual warehouses.
- Category: Cloud data warehouse.
- Related terms: virtual warehouse, micro-partitions, clustering, time travel, zero-copy clone, stage, semi-structured data.

## 4. Why It Exists

Traditional warehouses often required heavy infrastructure management.

Snowflake exists to provide:

- managed storage and compute
- SQL analytics
- independent workload scaling
- easier data sharing
- semi-structured data support
- governance and access control
- pay-for-usage cloud model

## 5. Where It Fits In A Data Platform

```text
Sources -> ingestion/ELT -> Snowflake storage -> virtual warehouses -> BI/SQL/ML users
```

Snowflake is often used for:

- executive dashboards
- finance reports
- customer analytics
- data marts
- governed enterprise analytics

## 6. How It Works Step By Step

1. Data is loaded into Snowflake tables.
2. Data is stored in optimized internal storage.
3. Compute runs in virtual warehouses.
4. A SQL query is submitted.
5. Cloud services manage parsing, optimization, metadata, and access control.
6. The virtual warehouse executes the query.
7. Results are returned and may be cached.
8. Compute can scale up/down or suspend when idle.

## 7. How To Use It Practically

Common workflow:

```sql
CREATE WAREHOUSE analyst_wh;
CREATE DATABASE analytics;
CREATE SCHEMA marts;

SELECT customer_region, SUM(revenue)
FROM marts.daily_sales
GROUP BY customer_region;
```

Practical concepts:

| Concept | Meaning |
|---|---|
| virtual warehouse | compute cluster for queries |
| database/schema/table | SQL organization |
| stage | place used to load/unload files |
| time travel | query older table versions |
| clustering | layout optimization for pruning |

## 8. Real-World Scenario

- Product/system: Finance analytics warehouse.
- Problem: Finance, marketing, and product teams run different workloads at the same time.
- How Snowflake helps: separate virtual warehouses can isolate workloads while sharing the same stored data.
- What would go wrong without it: one team query can slow another team's critical reporting.

## 9. System Design Angle

Use Snowflake when:

- business SQL/BI is central
- managed warehouse experience matters
- teams need workload isolation
- semi-structured data is common
- data sharing/governance matters

Be careful with:

- warehouse sizing
- auto-suspend settings
- query cost
- clustering cost
- role/access design

## 10. Trade-offs

| Pros | Cons |
|---|---|
| managed warehouse | cloud cost must be controlled |
| storage/compute separation | platform-specific features |
| workload isolation | tuning still needed |
| strong SQL/BI workflow | data copied into platform storage |
| time travel/cloning features | governance setup can be complex |

## 11. Failure Modes

- Failure: Warehouse left running.
- Symptom: unnecessary compute cost.
- Recovery: suspend warehouse.
- Prevention: auto-suspend and monitoring.

- Failure: Poorly filtered queries.
- Symptom: slow scans and high cost.
- Recovery: optimize SQL and table layout.
- Prevention: query review and marts.

- Failure: Bad role design.
- Symptom: users see too much or too little data.
- Recovery: fix grants.
- Prevention: least-privilege access model.

## 12. Common Mistakes

- Mistake: Making one giant warehouse for everything.
- Why it is wrong: cost and workload isolation suffer.
- Better approach: size warehouses by workload and concurrency.

- Mistake: Ignoring auto-suspend.
- Why it is wrong: idle compute can still cost money.
- Better approach: configure warehouse lifecycle carefully.

## 13. Mini Example

```text
BI warehouse:
  small/medium compute for dashboards

ETL warehouse:
  larger compute for transformations

Both read the same underlying data.
```

## 14. Interview Questions

1. What is Snowflake?
2. What does separation of storage and compute mean?
3. What is a virtual warehouse?
4. How does Snowflake support workload isolation?
5. How would you control Snowflake cost?

## 15. Interview Speak

"Snowflake is a managed cloud warehouse with separated storage and compute. Data is stored centrally while virtual warehouses provide independent compute for different workloads. I would use it for governed BI and analytics, with careful warehouse sizing, auto-suspend, role design, and table/query optimization."

## 16. Quick Recall

- One-line summary: Snowflake is managed SQL analytics with separate compute warehouses.
- Three keywords: virtual warehouse, managed, workload isolation.
- One trap: Leaving compute running or oversized.
- One memory trick: Shared storage, separate worker teams.
