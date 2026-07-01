# Topic 207: BigQuery

## 1. Goal

Understand BigQuery as GCP's serverless data warehouse.

## 2. Baby Intuition

BigQuery is a huge managed SQL engine where you focus on tables and queries instead of managing warehouse servers.

## 3. What It Is

- Simple definition: BigQuery is GCP's serverless data warehouse.
- Technical definition: BigQuery is a managed analytical database service for large-scale SQL queries, columnar storage, streaming/batch ingestion, and integration with the Google Cloud data ecosystem.
- Category: Cloud data warehouse.
- Related terms: dataset, table, partition, clustering, slots, external table, scheduled query, BI.

## 4. Why It Exists

Teams need:

- fast SQL over large data
- managed warehouse operations
- BI dashboards
- ad hoc analysis
- integration with Dataflow/Pub/Sub/Cloud Storage
- cost and access controls

BigQuery removes much of the cluster management from warehouse analytics.

## 5. Where It Fits In A Data Platform

```text
Cloud Storage / Pub/Sub / Dataflow / Dataproc / SaaS
  -> BigQuery tables
  -> SQL, BI, ML, reporting
```

## 6. How It Works Step By Step

1. Data is loaded, streamed, or queried externally.
2. Tables are stored in optimized columnar format.
3. Users submit SQL.
4. BigQuery plans distributed execution.
5. It scans needed columns/partitions.
6. Workers process joins/aggregations.
7. Results return or write to destination table.

## 7. How To Use It Practically

Good practices:

- partition large tables by date/time/range where useful
- cluster by frequent filters
- avoid `SELECT *`
- monitor scanned bytes and job cost
- use authorized views/row policies for security
- create marts/aggregates for dashboards

Example:

```sql
SELECT event_date, COUNT(*) AS events
FROM analytics.events
WHERE event_date >= DATE '2026-07-01'
GROUP BY event_date;
```

## 8. Real-World Scenario

- Product/system: Product analytics warehouse.
- Problem: Analysts query billions of events by day, country, and app version.
- How BigQuery helps: serverless SQL and partitioned/clustered tables support large analytical queries.
- What would go wrong without filters: full-table scans become slow and costly.

## 9. System Design Angle

Use BigQuery when:

- GCP-native warehouse analytics is needed
- serverless SQL is desired
- BI and ad hoc analytics are important
- Dataflow/Pub/Sub integrations matter

Be careful with:

- partition filters
- selected columns
- cost model/capacity choice
- access control
- streaming vs batch ingestion design

## 10. Trade-offs

| Pros | Cons |
|---|---|
| serverless warehouse | careless scans cost money |
| strong GCP integration | cloud-specific platform |
| good for BI/ad hoc SQL | query design still matters |
| partitioning/clustering | not an OLTP database |
| external/lake integrations | repeated transformations should be modeled |

## 11. Failure Modes

- Failure: Full table scan.
- Symptom: high cost/latency.
- Recovery: add filters, partitioning, clustering.
- Prevention: query standards and cost alerts.

- Failure: Bad permissions.
- Symptom: sensitive data exposure or blocked users.
- Recovery: fix IAM/policies.
- Prevention: least privilege and data classification.

- Failure: Dashboard repeats heavy raw query.
- Symptom: slow and costly BI.
- Recovery: materialized view/mart/aggregate.
- Prevention: model dashboard tables.

## 12. Common Mistakes

- Mistake: Using BigQuery like OLTP.
- Why it is wrong: it is optimized for analytical scans, not high-frequency row transactions.
- Better approach: use operational databases for OLTP.

- Mistake: Letting every analyst query raw events directly.
- Why it is wrong: cost and metric inconsistency grow.
- Better approach: build curated marts and semantic models.

## 13. Mini Example

```text
Pub/Sub events
  -> Dataflow validation/enrichment
  -> BigQuery partitioned events table
  -> daily aggregates for dashboard
```

## 14. Interview Questions

1. What is BigQuery?
2. Why is it called serverless?
3. How do partitioning and clustering help?
4. How do you control BigQuery cost?
5. BigQuery vs Dataproc?

## 15. Interview Speak

"BigQuery is GCP's serverless cloud data warehouse. I would use it for analytical SQL, BI, and ad hoc queries, designing large tables with partitioning and clustering, avoiding unnecessary scans, modeling marts for repeated dashboards, and controlling access and cost."

## 16. Quick Recall

- One-line summary: BigQuery is GCP serverless SQL analytics.
- Three keywords: serverless, partitioning, scanned bytes.
- One trap: Costly full scans.
- One memory trick: Managed SQL warehouse without choosing servers.
