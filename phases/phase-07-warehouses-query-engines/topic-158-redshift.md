# Topic 158: Redshift

## 1. Goal

Understand Amazon Redshift as AWS's cloud data warehouse.

## 2. Baby Intuition

Redshift is like a warehouse built from many worker nodes that split analytical SQL work.

It is designed for business queries over large structured datasets.

## 3. What It Is

- Simple definition: Redshift is a cloud data warehouse on AWS.
- Technical definition: Amazon Redshift is an MPP analytical database service that stores and queries structured/semi-structured data using SQL, with provisioned and serverless deployment options depending on setup.
- Category: Cloud data warehouse.
- Related terms: MPP, columnar storage, distribution style, sort key, Spectrum, concurrency scaling, RA3.

## 4. Why It Exists

AWS users need a managed warehouse for:

- BI dashboards
- reporting
- SQL analytics
- data marts
- integration with S3 data lakes
- scalable query processing

Redshift reduces the burden of managing a traditional on-prem warehouse.

## 5. Where It Fits In A Data Platform

```text
AWS sources / S3 / Glue / Kinesis / databases
  -> Redshift
  -> BI tools / SQL users / reporting
```

Redshift can store data internally and also query data in S3 through external table integrations.

## 6. How It Works Step By Step

1. Data is loaded into Redshift tables.
2. Tables use columnar storage.
3. Data distribution controls how rows are spread across nodes.
4. Sort keys help skip data and improve joins/ranges.
5. User submits SQL.
6. Query planner creates distributed execution steps.
7. Worker nodes scan, join, aggregate, and exchange data.
8. Results return to the client.

## 7. How To Use It Practically

Important design choices:

| Concept | Meaning |
|---|---|
| distribution style | how rows are placed across compute nodes |
| sort key | column order used for scan pruning |
| workload management | controls query queues/resources |
| Spectrum | query data in S3 |
| COPY | common bulk load command |

Example:

```sql
SELECT date_trunc('month', order_date) AS month, SUM(amount)
FROM fact_orders
GROUP BY 1;
```

## 8. Real-World Scenario

- Product/system: AWS retail data warehouse.
- Problem: Orders and clickstream data are stored in S3 and warehouse tables for BI.
- How Redshift helps: internal warehouse tables support repeated reporting; external S3 queries support lake access.
- What would go wrong without tuning: poor distribution/sort choices can make joins and scans slow.

## 9. System Design Angle

Use Redshift when:

- AWS is the main cloud
- SQL warehouse workloads are central
- data lives in S3 and AWS services
- BI/reporting needs managed MPP execution

Be careful with:

- distribution keys
- sort keys
- vacuum/analyze style maintenance where applicable
- workload queues/concurrency
- query cost and storage design

## 10. Trade-offs

| Pros | Cons |
|---|---|
| strong AWS integration | physical design choices matter |
| MPP SQL warehouse | poor distribution causes data movement |
| S3 lake integration | operational tuning still exists |
| good for BI/reporting | workload isolation must be planned |

## 11. Failure Modes

- Failure: Bad distribution key.
- Symptom: large data redistribution during joins.
- Recovery: redesign distribution or table layout.
- Prevention: choose keys from join patterns.

- Failure: Missing statistics.
- Symptom: poor query plans.
- Recovery: analyze/update stats.
- Prevention: maintenance automation.

- Failure: Too many concurrent heavy queries.
- Symptom: queueing and slow dashboards.
- Recovery: workload management/concurrency scaling.
- Prevention: isolate workloads and create aggregates.

## 12. Common Mistakes

- Mistake: Ignoring distribution design.
- Why it is wrong: MPP joins can become network-heavy.
- Better approach: colocate common join keys where useful.

- Mistake: Loading raw data but not modeling marts.
- Why it is wrong: every dashboard repeats expensive transformations.
- Better approach: build fact/dimension and aggregate tables.

## 13. Mini Example

```text
Orders join customers on customer_id.

If both large tables are distributed by customer_id,
workers can join more locally.

If not, data may shuffle across nodes.
```

## 14. Interview Questions

1. What is Redshift?
2. What is MPP?
3. Why do distribution keys matter?
4. What are sort keys?
5. How does Redshift connect with S3?

## 15. Interview Speak

"Redshift is AWS's managed MPP data warehouse. For performance, I would pay attention to distribution style, sort keys, table statistics, workload management, and S3 integration. Poor physical design can cause unnecessary data movement and slow joins."

## 16. Quick Recall

- One-line summary: Redshift is AWS MPP SQL warehousing.
- Three keywords: distribution, sort key, S3.
- One trap: Ignoring data movement in joins.
- One memory trick: Put join partners on the same workers when possible.
