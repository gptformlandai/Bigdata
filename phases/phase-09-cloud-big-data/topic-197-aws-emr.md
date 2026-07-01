# Topic 197: AWS EMR

## 1. Goal

Understand Amazon EMR as managed big data cluster service on AWS.

## 2. Baby Intuition

EMR is AWS helping you run Hadoop/Spark-style clusters without building every server manually.

You bring the job; EMR manages much of the cluster setup.

## 3. What It Is

- Simple definition: EMR is a managed service for running big data frameworks like Spark and Hadoop on AWS.
- Technical definition: Amazon EMR provisions and manages clusters or runtime environments for distributed data processing frameworks such as Apache Spark, Hadoop, Hive, Presto/Trino-style engines, and related ecosystem tools.
- Category: Managed big data processing.
- Related terms: Spark, Hadoop, cluster, node, step, bootstrap action, autoscaling, S3, YARN.

## 4. Why It Exists

Running big data clusters manually is operationally heavy:

- install software
- manage nodes
- scale capacity
- configure storage
- monitor jobs
- handle failures

EMR exists to simplify running distributed processing on AWS.

## 5. Where It Fits In A Data Platform

```text
S3 data lake
  -> EMR Spark/Hive jobs
  -> curated S3/lakehouse tables or warehouse outputs
```

EMR is compute. S3 is commonly the storage layer.

## 6. How It Works Step By Step

1. Choose framework/runtime and cluster configuration.
2. EMR provisions nodes or runtime environment.
3. Jobs are submitted as steps or through notebooks/APIs.
4. Spark/Hive/etc. reads data from S3/HDFS/other sources.
5. Distributed tasks process data.
6. Output is written back to S3 or downstream systems.
7. Cluster may terminate or stay running depending on workload.

## 7. How To Use It Practically

Common EMR patterns:

| Pattern | Use |
|---|---|
| transient cluster | create cluster per batch job, terminate after |
| long-running cluster | shared interactive/recurring workloads |
| EMR with S3 | data lake processing |
| EMR notebooks | exploration and development |
| autoscaling | adjust capacity to workload |

Practical advice:

- keep data in S3 for durability
- tune Spark jobs like normal Spark
- use transient clusters for cost control where possible
- separate dev and production workloads
- monitor failed steps and logs

## 8. Real-World Scenario

- Product/system: Nightly event ETL.
- Problem: Process 10 TB of clickstream data and write daily aggregates.
- How EMR helps: Spark cluster reads S3 raw data, transforms it, writes curated Parquet outputs, then cluster terminates.
- What would go wrong without cost control: idle clusters waste money.

## 9. System Design Angle

Use EMR when:

- Spark/Hadoop ecosystem jobs are needed on AWS
- data lives in S3
- cluster-level control matters
- workloads are batch/heavy distributed processing

Consider alternatives:

- AWS Glue for serverless Spark-style ETL
- Databricks for managed lakehouse notebooks/jobs
- Athena for serverless SQL over S3
- Redshift for warehouse BI

## 10. Trade-offs

| Pros | Cons |
|---|---|
| managed cluster setup | still needs Spark/cluster tuning |
| flexible big data frameworks | idle cluster cost |
| good S3 integration | operational choices remain |
| supports large batch jobs | startup time for transient clusters |
| configurable runtime | security/networking setup required |

## 11. Failure Modes

- Failure: Spark job out of memory.
- Symptom: failed EMR step.
- Recovery: tune partitions/memory/executors.
- Prevention: test and monitor Spark metrics.

- Failure: Cluster left running.
- Symptom: unnecessary cost.
- Recovery: terminate cluster.
- Prevention: auto-termination and tags.

- Failure: S3 permission issue.
- Symptom: job cannot read/write data.
- Recovery: fix IAM role/policy.
- Prevention: least-privilege tested roles.

## 12. Common Mistakes

- Mistake: Thinking EMR automatically makes bad Spark code fast.
- Why it is wrong: Spark tuning still matters.
- Better approach: tune joins, shuffles, partitions, memory, and file layout.

- Mistake: Using long-running clusters for occasional jobs.
- Why it is wrong: idle compute costs money.
- Better approach: use transient clusters or serverless alternatives.

## 13. Mini Example

```text
daily job:
create EMR cluster
run Spark ETL step
write Parquet to S3
terminate cluster
```

## 14. Interview Questions

1. What is EMR?
2. How does EMR relate to Spark?
3. EMR vs Glue?
4. Why use S3 with EMR?
5. How do you control EMR cost?

## 15. Interview Speak

"EMR is AWS managed big data compute for frameworks like Spark and Hadoop. I would use it for large distributed batch processing over S3 data, while managing cost with transient clusters/autoscaling and reliability with logs, retries, IAM, and Spark tuning."

## 16. Quick Recall

- One-line summary: EMR runs managed Spark/Hadoop-style clusters on AWS.
- Three keywords: cluster, Spark, S3.
- One trap: Leaving clusters idle.
- One memory trick: AWS-managed big data workshop.
