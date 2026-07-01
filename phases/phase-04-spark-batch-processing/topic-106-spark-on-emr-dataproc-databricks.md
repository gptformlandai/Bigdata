# Topic 106: Spark On EMR / Dataproc / Databricks

## 1. Goal

Understand how managed Spark platforms fit into real-world data engineering.

## 2. Baby Intuition

Running Spark yourself is like owning and maintaining a factory.

Managed platforms rent you a factory with many operations already handled.

You still need to write good jobs, but the platform helps with cluster setup, scaling, notebooks, libraries, and monitoring.

## 3. What It Is

- Simple definition: EMR, Dataproc, and Databricks are managed platforms for running Spark.
- Technical definition: Amazon EMR, Google Cloud Dataproc, and Databricks are managed data processing platforms that provide Spark clusters/jobs, integrations with cloud storage, monitoring, scaling, security, and ecosystem tooling.
- Category: Managed Spark/cloud data platform.
- Related terms: cluster, job, notebook, autoscaling, S3, GCS, DBFS, metastore, lakehouse.

## 4. Why It Exists

Self-managed Spark clusters require:

- installation
- upgrades
- scaling
- security
- dependencies
- monitoring
- failure handling
- cluster lifecycle management

Managed platforms reduce operational burden.

## 5. Where It Fits In A Data Platform

```text
Cloud storage -> Managed Spark platform -> curated tables/features/reports
```

Examples:

- EMR with S3
- Dataproc with GCS
- Databricks with cloud object storage and Delta Lake

## 6. How It Works Step By Step

Typical managed Spark job:

1. Store data in cloud object storage.
2. Create or configure Spark cluster/job.
3. Attach libraries/dependencies.
4. Submit notebook or job script.
5. Platform launches resources.
6. Spark processes data.
7. Output is written to storage/tables.
8. Cluster may auto-terminate.

## 7. How To Use It Practically

EMR mental model:

```text
AWS Spark cluster that reads/writes S3
```

Dataproc mental model:

```text
GCP managed Spark/Hadoop cluster that reads/writes GCS
```

Databricks mental model:

```text
Lakehouse platform with managed Spark, notebooks, jobs, Delta Lake, and optimized runtime
```

Common practical concerns:

- cluster size
- autoscaling
- instance type
- spot/preemptible nodes
- libraries
- IAM/service accounts
- logs
- job retries
- cost controls

## 8. Real-World Scenario

- Product/system: Modern cloud data lake.
- Problem: Team wants daily Spark ETL without managing Hadoop/YARN manually.
- How managed Spark helps: Platform provisions clusters, integrates with storage, and provides job monitoring.
- What would go wrong without it: Team spends more time managing infrastructure than building pipelines.

## 9. System Design Angle

Choose managed platforms when:

- cloud is already used
- team wants less cluster ops
- workloads are batch ETL/SQL/ML
- autoscaling/cost controls are needed
- governance/integration matters

Compare:

- EMR: flexible AWS managed Hadoop/Spark ecosystem.
- Dataproc: GCP managed Spark/Hadoop.
- Databricks: higher-level lakehouse/Spark platform with notebooks/jobs/Delta features.

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| less operations | platform cost |
| cloud storage integration | vendor-specific behavior |
| autoscaling/job tooling | configuration still matters |
| notebooks and monitoring | lock-in considerations |

## 11. Failure Modes

- Failure: Cluster under-sized.
- Symptom: slow jobs or OOM.
- Recovery: tune cluster/job.
- Prevention: workload sizing.

- Failure: Cloud permissions missing.
- Symptom: cannot read/write storage.
- Recovery: fix IAM/service account.
- Prevention: standard access patterns.

- Failure: Cost runaway.
- Symptom: large bill.
- Recovery: terminate clusters and tune jobs.
- Prevention: auto-termination, budgets, job clusters.

## 12. Common Mistakes

- Mistake: Thinking managed Spark removes Spark tuning.
- Why it is wrong: bad joins, skew, small files, and memory issues still happen.
- Better approach: tune jobs and use platform features.

- Mistake: Leaving clusters running.
- Why it is wrong: cost keeps accumulating.
- Better approach: auto-terminate and use job clusters.

## 13. Mini Example

Cloud Spark pattern:

```text
S3/GCS/ADLS raw data
  -> managed Spark job
  -> curated Parquet/Delta/Iceberg table
  -> BI/ML consumers
```

## 14. Interview Questions

1. Why use managed Spark platforms?
2. EMR vs Dataproc vs Databricks?
3. Does managed Spark remove tuning?
4. How do you control cost?
5. How does Spark use cloud object storage?

## 15. Interview Speak

"Managed Spark platforms like EMR, Dataproc, and Databricks reduce cluster operations by handling provisioning, integration, monitoring, and scaling. Spark still needs good data layout, partitioning, memory, and join tuning. I would choose based on cloud provider, lakehouse needs, governance, cost model, and team workflow."

## 16. Quick Recall

- One-line summary: Managed Spark platforms run Spark with less infrastructure burden.
- Three keywords: EMR, Dataproc, Databricks.
- One trap: Thinking managed means no tuning.
- One memory trick: Managed platforms rent you the Spark workshop.
