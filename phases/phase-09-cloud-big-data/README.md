# Phase 9: Cloud Big Data

Phase 9 teaches how Big Data platforms are built on AWS, GCP, and Azure.

The mental model is:

```text
cloud storage holds data
  -> managed compute processes data
  -> managed streaming moves live events
  -> warehouses/query services serve analytics
  -> IAM, encryption, networking, and cost controls keep it production-safe
```

Cloud Big Data is not about memorizing every button in every cloud console. It is about knowing which managed service fits which part of a data platform.

## Topics

| # | Topic | Status |
|---:|---|---|
| 196 | AWS S3 | Complete |
| 197 | AWS EMR | Complete |
| 198 | AWS Glue | Complete |
| 199 | AWS Athena | Complete |
| 200 | AWS Kinesis | Complete |
| 201 | AWS Redshift | Complete |
| 202 | AWS Lambda for data | Complete |
| 203 | GCP Cloud Storage | Complete |
| 204 | GCP Dataproc | Complete |
| 205 | GCP Dataflow | Complete |
| 206 | GCP Pub/Sub | Complete |
| 207 | BigQuery | Complete |
| 208 | Azure Data Lake Storage | Complete |
| 209 | Azure Synapse | Complete |
| 210 | Azure Event Hubs | Complete |
| 211 | Azure Databricks | Complete |
| 212 | Cloud cost optimization | Complete |
| 213 | IAM and security | Complete |
| 214 | Encryption at rest and in transit | Complete |
| 215 | VPC/networking basics for data platforms | Complete |

## Phase Goal

By the end of this phase, you should be able to explain:

- how AWS, GCP, and Azure map to common Big Data platform layers
- when to use object storage, managed Spark, serverless SQL, streaming services, warehouses, and serverless functions
- how cloud data lake and warehouse architectures are commonly designed
- why IAM, encryption, networking, and cost controls are not optional production details
- how to compare similar services across clouds at a high level

## Suggested Study Flow

1. Read Topics 196-202 for AWS Big Data building blocks.
2. Read Topics 203-207 for GCP Big Data building blocks.
3. Read Topics 208-211 for Azure Big Data building blocks.
4. Read Topics 212-215 for cross-cloud production foundations.
5. Finish with `phase-09-review.md`.
