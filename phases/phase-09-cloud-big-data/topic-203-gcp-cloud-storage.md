# Topic 203: GCP Cloud Storage

## 1. Goal

Understand Google Cloud Storage as the object storage foundation for GCP data lakes.

## 2. Baby Intuition

Cloud Storage is GCP's cloud file/object warehouse.

Data files land in buckets, then services like Dataproc, Dataflow, BigQuery, and Vertex AI can use them.

## 3. What It Is

- Simple definition: Cloud Storage is GCP object storage.
- Technical definition: Google Cloud Storage stores objects in buckets and is commonly used for data lakes, file landing zones, backups, logs, analytics datasets, and ML assets.
- Category: Cloud object storage.
- Related terms: bucket, object, prefix, storage class, lifecycle, IAM, encryption, data lake.

## 4. Why It Exists

Big Data platforms need scalable shared storage for:

- raw events
- batch files
- logs
- model artifacts
- Parquet/Avro/JSON/CSV data
- archival data

Cloud Storage provides durable object storage that many GCP services can read/write.

## 5. Where It Fits In A Data Platform

```text
sources/logs/events
  -> Cloud Storage raw bucket
  -> Dataflow/Dataproc transforms
  -> curated Cloud Storage or BigQuery
  -> BI/ML/analytics
```

## 6. How It Works Step By Step

1. Create a bucket.
2. Write objects with structured paths/prefixes.
3. Control access with IAM.
4. Encrypt data.
5. Apply lifecycle policies for cost/retention.
6. Process data with Dataproc/Dataflow.
7. Query/load curated data with BigQuery.

## 7. How To Use It Practically

Good practices:

- separate raw, clean, and curated buckets/prefixes
- use columnar formats for analytics
- partition paths by date/time where useful
- avoid small files
- set lifecycle policies
- apply IAM least privilege
- classify sensitive data

Example:

```text
gs://company-lake/bronze/clicks/dt=2026-07-01/part-0001.parquet
```

## 8. Real-World Scenario

- Product/system: Mobile app event lake.
- Problem: App events need durable storage for replay and analytics.
- How Cloud Storage helps: raw events land in buckets; Dataflow/Dataproc cleans them; BigQuery serves analytics.
- What would go wrong without layout: BigQuery external queries or processing jobs scan too much and become hard to govern.

## 9. System Design Angle

Use Cloud Storage when:

- GCP data lake storage is needed
- raw immutable files must be retained
- multiple GCP services need shared data
- batch processing and replay matter

Be careful with:

- IAM
- bucket organization
- lifecycle costs
- file size/layout
- encryption and sensitive data

## 10. Trade-offs

| Pros | Cons |
|---|---|
| scalable object storage | not a warehouse by itself |
| integrates with GCP analytics | object layout affects performance |
| good for raw archive | small files hurt processing |
| lifecycle management | governance must be added |
| shared storage layer | table metadata may need catalog/lakehouse tools |

## 11. Failure Modes

- Failure: Bad IAM.
- Symptom: jobs cannot read/write or users over-access data.
- Recovery: fix roles/policies.
- Prevention: least privilege.

- Failure: Poor file layout.
- Symptom: slow processing/querying.
- Recovery: rewrite/compact data.
- Prevention: partition and file-size standards.

- Failure: No lifecycle policy.
- Symptom: storage cost grows.
- Recovery: archive/delete old data where allowed.
- Prevention: retention design.

## 12. Common Mistakes

- Mistake: Treating Cloud Storage as a database.
- Why it is wrong: it stores objects; query/transaction behavior comes from engines/table formats.
- Better approach: pair it with BigQuery, Dataproc, Dataflow, or lakehouse formats.

- Mistake: Mixing raw and curated data without boundaries.
- Why it is wrong: users may consume untrusted data accidentally.
- Better approach: separate zones and permissions.

## 13. Mini Example

```text
raw:
gs://lake/bronze/orders/json/

clean:
gs://lake/silver/orders_parquet/dt=2026-07-01/

analytics:
BigQuery external/native table reads curated output
```

## 14. Interview Questions

1. What is GCP Cloud Storage?
2. How is it used in a data lake?
3. How do Dataflow and Dataproc use it?
4. How do you secure buckets?
5. Why do file format and layout matter?

## 15. Interview Speak

"Cloud Storage is GCP's object storage foundation for data lakes. I would store raw and curated data in clear zones, process it with Dataflow or Dataproc, serve analytics through BigQuery, and manage IAM, encryption, lifecycle policies, partitioning, and file sizes carefully."

## 16. Quick Recall

- One-line summary: Cloud Storage is GCP object storage for data lakes.
- Three keywords: bucket, object, data lake.
- One trap: No governance/layout on raw buckets.
- One memory trick: GCP cloud warehouse for objects.
