# Phase 9 Review: Cloud Big Data

## 1. Phase Summary

Phase 9 explains how Big Data platforms are built with managed cloud services across AWS, GCP, and Azure.

The core idea:

```text
object storage is the lake
managed compute transforms data
streaming services move live events
warehouses/query services serve analytics
security, networking, encryption, and cost controls make it production-ready
```

If you remember only one sentence:

```text
Cloud Big Data is about choosing the right managed service for storage, compute, streaming, SQL, security, and cost.
```

## 2. Cloud Service Map

| Platform Layer | AWS | GCP | Azure |
|---|---|---|---|
| object/data lake storage | S3 | Cloud Storage | ADLS |
| managed Spark/Hadoop | EMR | Dataproc | Azure Databricks / Synapse Spark |
| serverless ETL | Glue | Dataflow for Beam-style processing | Synapse/Data Factory/Databricks patterns |
| streaming ingestion | Kinesis | Pub/Sub | Event Hubs |
| warehouse | Redshift | BigQuery | Synapse dedicated SQL |
| serverless lake SQL | Athena | BigQuery external/lake patterns | Synapse serverless SQL |
| serverless functions | Lambda | Cloud Functions | Azure Functions |
| BI ecosystem | QuickSight/partners | Looker/partners | Power BI |

## 3. Common Cloud Data Lake Pattern

```text
Sources
  -> streaming/batch ingestion
  -> cloud object storage raw zone
  -> managed compute cleans/transforms data
  -> curated lakehouse/warehouse tables
  -> SQL/BI/ML/product consumers
```

AWS example:

```text
apps -> Kinesis -> S3 bronze -> Glue/EMR -> S3 silver/gold -> Athena/Redshift
```

GCP example:

```text
apps -> Pub/Sub -> Dataflow -> Cloud Storage/BigQuery -> Looker/BI
```

Azure example:

```text
apps -> Event Hubs -> ADLS bronze -> Databricks/Synapse -> Power BI
```

## 4. AWS Quick Recall

| Service | One-Line Meaning | Best Fit |
|---|---|---|
| S3 | object storage for data lakes | raw/curated file storage |
| EMR | managed Spark/Hadoop clusters | large distributed processing |
| Glue | catalog and serverless ETL | AWS-native metadata/ETL |
| Athena | serverless SQL over S3 | ad hoc lake queries |
| Kinesis | managed event streaming | AWS event ingestion |
| Redshift | cloud data warehouse | BI/reporting warehouse |
| Lambda | small serverless functions | event glue/triggers |

## 5. GCP Quick Recall

| Service | One-Line Meaning | Best Fit |
|---|---|---|
| Cloud Storage | object storage for data lakes | raw/curated file storage |
| Dataproc | managed Spark/Hadoop | open-source big data jobs |
| Dataflow | managed Apache Beam | batch/stream pipelines |
| Pub/Sub | managed messaging | event-driven ingestion |
| BigQuery | serverless data warehouse | SQL analytics and BI |

## 6. Azure Quick Recall

| Service | One-Line Meaning | Best Fit |
|---|---|---|
| ADLS | Azure data lake storage | secure lake storage |
| Synapse | integrated SQL/Spark/lake analytics | Azure analytics workspace |
| Event Hubs | managed event streaming | Azure event ingestion |
| Azure Databricks | managed Spark/lakehouse | Delta/Spark data engineering |

## 7. Storage Design Checklist

For S3, Cloud Storage, or ADLS:

- separate raw, clean, and curated zones
- use clear prefixes/paths
- use columnar formats for curated analytics
- avoid tiny files
- partition by common filters
- enable encryption
- restrict public access
- define lifecycle/retention
- classify PII/sensitive data
- use table formats/catalogs for lakehouse tables

## 8. Compute Choice Guide

| Need | Better Fit |
|---|---|
| Spark/Hadoop compatibility | EMR, Dataproc, Databricks |
| SQL BI warehouse | Redshift, BigQuery, Synapse |
| ad hoc SQL over lake files | Athena, Synapse serverless SQL, BigQuery external patterns |
| streaming ETL | Dataflow, Flink, Databricks streaming, Kinesis consumers |
| lightweight event reaction | Lambda/Cloud Functions/Azure Functions |
| Python/SQL analytics transformations | dbt/warehouse SQL/Spark depending on scale |

## 9. Streaming Choice Guide

| Cloud | Streaming Service | Mental Model |
|---|---|---|
| AWS | Kinesis | managed event stream/shards |
| GCP | Pub/Sub | topics and subscriptions |
| Azure | Event Hubs | event stream with partitions and consumer groups |

Common streaming design rules:

- choose partition key carefully
- monitor consumer lag
- handle duplicates
- validate schemas
- archive raw events
- create DLQ/quarantine path
- define ordering requirements clearly

## 10. Cost Optimization Checklist

Cost drivers:

- idle clusters
- oversized warehouses
- full table scans
- tiny files
- duplicate datasets
- long retention
- cross-region transfer
- overprovisioned streaming capacity

Controls:

- tags and owners
- budgets and alerts
- auto-suspend/auto-terminate
- autoscaling
- partitioning and columnar formats
- lifecycle policies
- aggregate/materialized tables for repeated dashboards
- right-sized compute
- query guardrails

Strong line:

> Optimize cost per useful data product, not just the cheapest resource.

## 11. Security Checklist

For every cloud data platform:

- use least-privilege IAM
- use service accounts/roles for jobs
- avoid hardcoded credentials
- separate environments
- separate data zones
- encrypt at rest
- enforce TLS/in-transit encryption
- audit access
- restrict sensitive data
- use private networking where needed
- manage keys carefully

## 12. IAM Mental Model

IAM answers:

```text
who can do what on which resource?
```

Examples:

```text
Glue job role can read raw/orders and write silver/orders.
It cannot delete the bucket or read unrelated PII.
```

Common trap:

```text
Giving admin permissions to pipeline jobs.
```

## 13. Encryption Mental Model

At rest:

```text
stored data is encrypted in buckets, disks, databases, and warehouses
```

In transit:

```text
data moving between services is encrypted, commonly using TLS
```

Key reminder:

```text
Encryption does not replace IAM.
```

## 14. Networking Mental Model

VPC/VNet is the private network boundary.

Important pieces:

- subnets
- routes
- firewalls/security groups
- private endpoints
- NAT
- peering
- VPN/dedicated connectivity

Strong line:

> Keep data-plane traffic private where possible and explicitly control ingress and egress.

## 15. Common Interview Questions

1. Design a data lake on AWS/GCP/Azure.
2. S3 vs Redshift vs Athena?
3. EMR vs Glue?
4. Dataproc vs Dataflow?
5. BigQuery vs Dataproc?
6. Synapse vs Databricks?
7. Kinesis vs Pub/Sub vs Event Hubs?
8. How do you secure a cloud data lake?
9. How do you reduce cloud data costs?
10. Encryption at rest vs in transit?
11. What is IAM least privilege?
12. What is a private endpoint?
13. Why avoid cross-region data movement?
14. How do you handle streaming duplicates?
15. How do you design raw/clean/curated zones?

## 16. Strong System Design Answer

Question:

> Design a cloud data platform for clickstream analytics and business reporting.

Strong answer:

"I would use object storage as the durable data lake foundation: S3 on AWS, Cloud Storage on GCP, or ADLS on Azure. Raw clickstream events would be ingested through a managed streaming service such as Kinesis, Pub/Sub, or Event Hubs and archived to the raw zone for replay.

For processing, I would use managed compute based on workload: Glue/EMR, Dataflow/Dataproc, or Databricks/Synapse. The pipeline would validate schemas, deduplicate, partition by event date, write curated columnar files or lakehouse tables, and create gold aggregates for BI.

For analytics, I would use a warehouse or query service such as Redshift, BigQuery, Synapse, or Athena depending on latency, cost, and query frequency. I would secure the platform with least-privilege IAM, encryption at rest and in transit, private networking where required, audit logs, and PII controls. I would control cost using tags, budgets, lifecycle policies, auto-termination, partitioning, clustering, and aggregate tables for repeated dashboards."

## 17. Hands-On Project

Build a cloud architecture diagram in notes:

1. Pick AWS, GCP, or Azure.
2. Define raw, clean, and curated storage zones.
3. Add one streaming ingestion service.
4. Add one batch processing service.
5. Add one warehouse/query serving service.
6. Add IAM roles/service accounts.
7. Add encryption and networking controls.
8. Add cost controls and monitoring.

Example AWS:

```text
Kinesis -> S3 bronze -> Glue/EMR -> S3 silver/gold -> Athena/Redshift
IAM roles + KMS + VPC endpoints + lifecycle policies + budgets
```

## 18. Quick Revision Cards

| Prompt | Answer |
|---|---|
| AWS object storage | S3 |
| GCP object storage | Cloud Storage |
| Azure data lake storage | ADLS |
| AWS Spark/Hadoop | EMR |
| GCP Spark/Hadoop | Dataproc |
| Azure Spark/lakehouse | Azure Databricks |
| AWS serverless SQL over S3 | Athena |
| GCP warehouse | BigQuery |
| Azure integrated analytics | Synapse |
| AWS streaming | Kinesis |
| GCP messaging | Pub/Sub |
| Azure streaming | Event Hubs |
| Cloud cost levers | tags, budgets, idle compute, scanned bytes |
| IAM principle | least privilege |
| At rest | stored data encryption |
| In transit | network/TLS encryption |
| VPC | private cloud network |
