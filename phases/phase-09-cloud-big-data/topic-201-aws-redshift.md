# Topic 201: AWS Redshift

## 1. Goal

Understand Amazon Redshift as AWS's managed cloud data warehouse.

## 2. Baby Intuition

Redshift is the AWS warehouse for business SQL.

It is built to answer large analytical questions over structured data.

## 3. What It Is

- Simple definition: Redshift is AWS's cloud data warehouse.
- Technical definition: Amazon Redshift is a managed analytical database service for SQL-based warehousing, using distributed processing, columnar storage, and AWS ecosystem integrations.
- Category: Cloud data warehouse.
- Related terms: MPP, columnar storage, distribution key, sort key, Spectrum, workload management, BI.

## 4. Why It Exists

Businesses need fast SQL reports:

- revenue dashboards
- customer analytics
- financial reporting
- product metrics
- data marts

Redshift exists to provide a managed AWS-native warehouse instead of building one manually.

## 5. Where It Fits In A Data Platform

```text
S3/data sources
  -> ingestion/ETL/ELT
  -> Redshift warehouse
  -> BI dashboards and analysts
```

It can also query data in S3 in certain patterns, often used with lake integrations.

## 6. How It Works Step By Step

1. Load data into Redshift tables or query external data.
2. Data is stored columnar for analytics.
3. Tables are distributed across compute.
4. Sort keys/layout help pruning.
5. Query planner creates distributed SQL plan.
6. Nodes scan, join, aggregate, and exchange data.
7. Results are returned to BI/users.

## 7. How To Use It Practically

Important concepts:

| Concept | Meaning |
|---|---|
| distribution style/key | how data is spread for joins |
| sort key | physical order for pruning/ranges |
| COPY | bulk load pattern |
| Spectrum/external tables | query S3 data |
| workload management | control query resources |

Good practice:

- model facts and dimensions
- choose distribution/sort based on queries
- use columnar compression
- monitor slow queries and queues
- avoid loading tiny files one by one

## 8. Real-World Scenario

- Product/system: AWS analytics warehouse.
- Problem: Business users need dashboards over orders, payments, and customer tables.
- How Redshift helps: modeled warehouse tables serve repeated BI queries efficiently.
- What would go wrong without design: bad distribution causes expensive data movement.

## 9. System Design Angle

Use Redshift when:

- AWS-native SQL warehouse is needed
- BI/reporting is central
- structured warehouse modeling matters
- data is frequently queried by analysts

Consider Athena when:

- data stays in S3
- ad hoc lake SQL is enough

Consider Spark/EMR/Glue when:

- heavy transformation over files is needed

## 10. Trade-offs

| Pros | Cons |
|---|---|
| AWS-native warehouse | physical design matters |
| good BI SQL support | cost/concurrency planning needed |
| columnar MPP analytics | not raw object storage |
| integrates with S3 | tuning required for large joins |

## 11. Failure Modes

- Failure: Bad distribution key.
- Symptom: large network redistribution.
- Recovery: redesign table.
- Prevention: choose based on join patterns.

- Failure: Query queue congestion.
- Symptom: dashboards slow.
- Recovery: workload management and scaling.
- Prevention: isolate workloads and aggregate repeated queries.

- Failure: Stale/missing stats.
- Symptom: poor plans.
- Recovery: update stats.
- Prevention: maintenance automation.

## 12. Common Mistakes

- Mistake: Loading raw unmodeled data only.
- Why it is wrong: every dashboard repeats heavy logic.
- Better approach: build facts, dimensions, and marts.

- Mistake: Ignoring sort/distribution choices.
- Why it is wrong: warehouse performance depends on physical design.
- Better approach: model from query and join patterns.

## 13. Mini Example

```text
S3 raw orders
  -> Glue/EMR/dbt transform
  -> Redshift fact_orders + dim_customer
  -> BI dashboard
```

## 14. Interview Questions

1. What is Redshift?
2. Redshift vs Athena?
3. Why do distribution keys matter?
4. What is a sort key?
5. How do you optimize Redshift cost/performance?

## 15. Interview Speak

"Redshift is AWS's managed data warehouse for SQL analytics. I would use it for modeled BI/reporting workloads, tune distribution and sort keys around query patterns, manage concurrency/cost, and integrate with S3 through ingestion or external table patterns."

## 16. Quick Recall

- One-line summary: Redshift is AWS's analytical SQL warehouse.
- Three keywords: MPP, distribution, BI.
- One trap: Treating physical design as optional.
- One memory trick: AWS business SQL warehouse.
