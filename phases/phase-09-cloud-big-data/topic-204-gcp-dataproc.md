# Topic 204: GCP Dataproc

## 1. Goal

Understand Dataproc as GCP's managed service for Spark/Hadoop-style processing.

## 2. Baby Intuition

Dataproc is GCP helping you run Spark/Hadoop jobs without building the cluster from scratch.

It is similar in spirit to AWS EMR.

## 3. What It Is

- Simple definition: Dataproc is managed Spark/Hadoop on Google Cloud.
- Technical definition: Google Cloud Dataproc provisions and manages clusters or serverless runtimes for open-source data processing frameworks such as Spark, Hadoop, Hive, and related tools.
- Category: Managed big data processing.
- Related terms: Spark, Hadoop, cluster, serverless batch, Cloud Storage, BigQuery connector, autoscaling.

## 4. Why It Exists

Teams use Spark/Hadoop ecosystems but do not want to manually:

- install clusters
- patch nodes
- configure networking
- scale workers
- operate YARN/Spark infrastructure

Dataproc provides managed execution for these workloads on GCP.

## 5. Where It Fits In A Data Platform

```text
Cloud Storage / BigQuery / sources
  -> Dataproc Spark jobs
  -> curated Cloud Storage / BigQuery / lakehouse tables
```

## 6. How It Works Step By Step

1. Configure cluster or serverless job.
2. Submit Spark/Hadoop/Hive job.
3. Dataproc provisions compute.
4. Job reads data from Cloud Storage/BigQuery/etc.
5. Distributed tasks process data.
6. Output is written to storage/warehouse.
7. Cluster/job resources scale or terminate based on setup.

## 7. How To Use It Practically

Common patterns:

| Pattern | Use |
|---|---|
| transient cluster | batch job then terminate |
| serverless batch | run Spark without managing cluster |
| long-running cluster | shared interactive workloads |
| Cloud Storage input/output | data lake processing |
| BigQuery connector | read/write warehouse data |

Good habits:

- tune Spark like normal Spark
- use transient/serverless for cost control
- keep data durable outside cluster
- monitor job logs and metrics
- avoid idle clusters

## 8. Real-World Scenario

- Product/system: Historical clickstream processing.
- Problem: Process years of Cloud Storage event files into curated Parquet and BigQuery tables.
- How Dataproc helps: Spark runs distributed transformations without self-managed Hadoop cluster.
- What would go wrong without tuning: shuffle-heavy Spark jobs may fail or cost too much.

## 9. System Design Angle

Use Dataproc when:

- Spark/Hadoop ecosystem jobs are needed on GCP
- data lake files must be processed at scale
- open-source compatibility matters
- more control than Dataflow is useful

Consider Dataflow when:

- Apache Beam streaming/batch pipelines fit
- fully managed stream processing is needed

Consider BigQuery SQL when:

- transformations are SQL-native in warehouse

## 10. Trade-offs

| Pros | Cons |
|---|---|
| managed Spark/Hadoop | Spark tuning still required |
| GCP integration | idle clusters cost money |
| flexible open-source stack | cluster config choices matter |
| good for heavy batch | job startup/config overhead |

## 11. Failure Modes

- Failure: Cluster under-sized.
- Symptom: slow/failing jobs.
- Recovery: resize/tune Spark.
- Prevention: capacity testing.

- Failure: Idle cluster.
- Symptom: wasted cost.
- Recovery: terminate.
- Prevention: auto-delete/transient jobs.

- Failure: Permission issue.
- Symptom: job cannot access buckets/BigQuery.
- Recovery: fix service account roles.
- Prevention: least-privilege service accounts.

## 12. Common Mistakes

- Mistake: Thinking managed cluster removes need for Spark knowledge.
- Why it is wrong: Spark logic, joins, shuffle, memory, and partitioning still matter.
- Better approach: tune jobs and data layout.

- Mistake: Choosing Dataproc for simple SQL transformations.
- Why it is wrong: BigQuery/dbt may be simpler.
- Better approach: choose compute based on workload.

## 13. Mini Example

```text
Dataproc Spark job:
read gs://lake/bronze/events/
clean and dedupe
write gs://lake/silver/events_parquet/
load/register in BigQuery
```

## 14. Interview Questions

1. What is Dataproc?
2. Dataproc vs Dataflow?
3. Dataproc vs BigQuery?
4. How do you control Dataproc cost?
5. Why store data outside the cluster?

## 15. Interview Speak

"Dataproc is GCP's managed Spark/Hadoop processing service. I would use it for large open-source big data jobs over Cloud Storage or BigQuery data, controlling cost with transient/serverless jobs and reliability through Spark tuning, monitoring, and proper service account permissions."

## 16. Quick Recall

- One-line summary: Dataproc runs managed Spark/Hadoop workloads on GCP.
- Three keywords: Spark, cluster, Cloud Storage.
- One trap: Idle clusters.
- One memory trick: GCP-managed Spark workshop.
