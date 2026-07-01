# Topic 157: BigQuery

## 1. Goal

Understand BigQuery as Google's serverless data warehouse.

## 2. Baby Intuition

BigQuery is like asking a huge managed SQL service a question without choosing servers first.

You upload or reference data, write SQL, and the platform handles the distributed execution.

## 3. What It Is

- Simple definition: BigQuery is a serverless cloud data warehouse.
- Technical definition: BigQuery is a managed analytical database on Google Cloud that separates storage and compute and runs distributed SQL queries without user-managed clusters.
- Category: Cloud data warehouse.
- Related terms: serverless warehouse, slots, columnar storage, partitioned tables, clustered tables, external tables, BI Engine.

## 4. Why It Exists

BigQuery exists to make large-scale SQL analytics easier:

- no cluster provisioning for basic usage
- fast scans over large datasets
- built-in SQL interface
- automatic distributed execution
- integration with Google Cloud data tools
- support for batch and streaming ingestion

## 5. Where It Fits In A Data Platform

```text
Cloud Storage / Pub/Sub / Dataflow / databases / SaaS
  -> BigQuery datasets and tables
  -> SQL analytics, BI, ML, reporting
```

Common use cases:

- product analytics
- log analytics
- marketing attribution
- finance dashboards
- data science exploration

## 6. How It Works Step By Step

1. Data is loaded into BigQuery tables or queried externally.
2. Tables are often partitioned and clustered.
3. User submits SQL.
4. BigQuery parses and optimizes the query.
5. Distributed workers scan columnar data.
6. Only required columns and partitions are read when possible.
7. Results are returned or written to a table.
8. Cost depends on pricing mode and workload configuration.

## 7. How To Use It Practically

Basic SQL:

```sql
SELECT event_date, COUNT(*) AS events
FROM analytics.events
WHERE event_date >= DATE '2026-07-01'
GROUP BY event_date;
```

Practical concepts:

| Concept | Meaning |
|---|---|
| dataset | namespace for tables |
| partitioned table | table split by date/range/ingestion time |
| clustered table | data organized by selected columns |
| slots | compute capacity concept |
| external table | query files outside native storage |

## 8. Real-World Scenario

- Product/system: Mobile app analytics.
- Problem: Billions of events need SQL exploration by date, country, and app version.
- How BigQuery helps: analysts use SQL over large event tables without managing clusters.
- What would go wrong without tuning: queries without date filters may scan too much data and cost more.

## 9. System Design Angle

Use BigQuery when:

- serverless warehouse simplicity matters
- Google Cloud ecosystem is already used
- ad hoc analytics and BI are common
- huge scan-based SQL workloads exist

Be careful with:

- partition filters
- scanned bytes
- slot/capacity planning
- nested/semi-structured data design
- table expiration and governance

## 10. Trade-offs

| Pros | Cons |
|---|---|
| serverless SQL | cost surprises from large scans |
| scales automatically for many workloads | less control than self-managed engines |
| strong GCP integration | cloud/provider coupling |
| good for ad hoc analytics | query design still matters |
| supports partitioning/clustering | streaming and storage choices affect cost |

## 11. Failure Modes

- Failure: Query scans full event table.
- Symptom: high cost and slow query.
- Recovery: add partition filters and optimize SQL.
- Prevention: require date filters for large tables.

- Failure: Bad clustering choice.
- Symptom: filters do not skip enough data.
- Recovery: adjust clustering based on query patterns.
- Prevention: review query logs.

- Failure: Permission misconfiguration.
- Symptom: user cannot access dataset or sees sensitive data.
- Recovery: fix IAM/table permissions.
- Prevention: governed access model.

## 12. Common Mistakes

- Mistake: Using `SELECT *` on huge tables.
- Why it is wrong: columnar warehouses charge/work by scanned data.
- Better approach: select only required columns.

- Mistake: Forgetting partition filters.
- Why it is wrong: a date table may scan years of data.
- Better approach: filter partition columns by default.

## 13. Mini Example

```text
Good:
SELECT user_id FROM events
WHERE event_date = '2026-07-01'

Risky:
SELECT * FROM events
```

## 14. Interview Questions

1. What is BigQuery?
2. What does serverless warehouse mean?
3. How do partitioning and clustering help?
4. How do you control query cost?
5. When would you use BigQuery vs Spark?

## 15. Interview Speak

"BigQuery is a serverless cloud data warehouse for large-scale SQL analytics. I would design large tables with partitioning and clustering, avoid unnecessary columns/scans, monitor cost, and use it for BI, ad hoc analysis, and GCP-integrated analytical workloads."

## 16. Quick Recall

- One-line summary: BigQuery is serverless distributed SQL analytics.
- Three keywords: serverless, partitioning, scanned data.
- One trap: Full-table scans from careless SQL.
- One memory trick: Ask SQL first, servers later never.
