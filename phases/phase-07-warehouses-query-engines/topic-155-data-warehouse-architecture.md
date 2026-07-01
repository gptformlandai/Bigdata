# Topic 155: Data Warehouse Architecture

## 1. Goal

Understand what a data warehouse is, why companies use it, and how its layers fit together.

## 2. Baby Intuition

A data warehouse is like a clean, organized reporting room for the business.

Raw systems may be messy, but the warehouse gives analysts trusted tables for questions like revenue, active users, orders, churn, and performance.

## 3. What It Is

- Simple definition: A data warehouse stores cleaned, structured data for analytics and reporting.
- Technical definition: A data warehouse is an analytical data platform optimized for SQL queries over historical, structured, and semi-structured business data.
- Category: OLAP storage and query system.
- Related terms: OLAP, BI, ETL, ELT, fact table, dimension table, star schema, MPP.

## 4. Why It Exists

Operational databases are built for transactions:

```text
insert order
update payment
change account status
```

Analysts need different questions:

```text
total revenue by month
top products by region
customer retention by cohort
fraud rate by payment method
```

Running these large analytical queries directly on production OLTP databases can slow the product. Warehouses solve this by copying and modeling data for analytics.

## 5. Where It Fits In A Data Platform

```text
Apps / OLTP DBs / logs / SaaS tools
  -> ingestion / CDC / batch loads
  -> raw/staging area
  -> transformations
  -> warehouse tables
  -> BI dashboards / analysts / data science
```

Common cloud warehouses:

- Snowflake
- BigQuery
- Redshift
- Synapse

## 6. How It Works Step By Step

1. Data is extracted from source systems.
2. Data lands in staging/raw tables.
3. Transformations clean, join, dedupe, and standardize it.
4. Modeled tables are created for business use.
5. Query optimizer plans SQL queries.
6. Distributed workers scan/process data.
7. Results are returned to dashboards or users.
8. Governance controls access and lineage.

## 7. How To Use It Practically

Typical warehouse layers:

| Layer | Meaning |
|---|---|
| staging/raw | source-like copied data |
| intermediate | cleaned and reusable logic |
| marts | team-specific business tables |
| semantic/gold | trusted metrics and dimensions |

Common table types:

- fact tables: events/transactions/measures
- dimension tables: descriptive context
- aggregate tables: precomputed summaries
- snapshot tables: state captured over time

## 8. Real-World Scenario

- Product/system: Retail reporting platform.
- Problem: Business wants revenue by product, store, channel, and date.
- How warehouse helps: source data is cleaned into facts and dimensions, then queried by BI tools.
- What would go wrong without it: analysts query production systems, duplicate logic, and produce inconsistent metrics.

## 9. System Design Angle

Clarify:

- data volume
- query concurrency
- freshness SLA
- dashboard latency
- cost constraints
- source systems
- access control/PII
- data modeling needs

Simple design:

```text
OLTP DBs -> CDC/batch ingestion -> warehouse staging -> dbt/Spark SQL transforms -> marts -> BI
```

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| fast business SQL | data duplication |
| trusted metrics | modeling effort |
| protects OLTP systems | freshness delay |
| governance and auditing | warehouse cost |
| historical analysis | pipeline maintenance |

## 11. Failure Modes

- Failure: Bad upstream data.
- Symptom: dashboard numbers wrong.
- Recovery: fix data and backfill.
- Prevention: validation and data quality checks.

- Failure: Query cost explosion.
- Symptom: high warehouse bill.
- Recovery: optimize queries/tables and budgets.
- Prevention: cost monitoring and workload controls.

- Failure: Metric definitions differ.
- Symptom: teams report different revenue numbers.
- Recovery: central semantic layer or certified marts.
- Prevention: governed definitions.

## 12. Common Mistakes

- Mistake: Treating warehouse as a raw dump only.
- Why it is wrong: users need clean business-ready tables.
- Better approach: create modeled layers and metric definitions.

- Mistake: Running every dashboard on raw event tables.
- Why it is wrong: slow and expensive.
- Better approach: create aggregates or marts for repeated use.

## 13. Mini Example

```text
orders fact:
order_id, customer_id, product_id, order_date, amount

date dimension:
date, week, month, quarter, year

Question:
revenue by month
```

## 14. Interview Questions

1. What is a data warehouse?
2. Why not query production databases directly?
3. What layers exist in a warehouse?
4. What is the difference between fact and dimension tables?
5. How would you design warehouse ingestion?

## 15. Interview Speak

"A warehouse is an OLAP system for trusted analytics. I would ingest data from operational systems into staging, transform it into modeled facts and dimensions, expose marts or semantic tables for BI, and optimize for query latency, concurrency, governance, freshness, and cost."

## 16. Quick Recall

- One-line summary: A warehouse is the organized SQL home for business analytics.
- Three keywords: OLAP, BI, modeled tables.
- One trap: Using production OLTP databases for heavy analytics.
- One memory trick: Warehouse is the business reporting room.
