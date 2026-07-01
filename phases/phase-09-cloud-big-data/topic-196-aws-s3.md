# Topic 196: AWS S3

## 1. Goal

Understand Amazon S3 as the core object storage layer for AWS data lakes.

## 2. Baby Intuition

S3 is like an unlimited cloud file warehouse.

You put objects into buckets, and data tools like Spark, Athena, Glue, Redshift, and ML jobs can read from it.

## 3. What It Is

- Simple definition: S3 is AWS object storage.
- Technical definition: Amazon S3 stores data as objects in buckets and is commonly used as durable, scalable storage for data lakes, backups, logs, analytics files, and application assets.
- Category: Cloud object storage.
- Related terms: bucket, object, key, prefix, storage class, lifecycle policy, versioning, encryption, IAM.

## 4. Why It Exists

Big Data needs storage that is:

- scalable
- durable
- accessible by many services
- cheaper than always-on databases for raw files
- good for logs, events, Parquet, CSV, JSON, Avro, images, and backups

S3 became a common foundation for AWS data lakes.

## 5. Where It Fits In A Data Platform

```text
applications/databases/logs/events
  -> S3 raw zone
  -> Glue/EMR/Spark transforms
  -> S3 curated zone or Redshift/warehouse
  -> Athena/BI/ML
```

Typical lake zones:

| Zone | Meaning |
|---|---|
| raw/bronze | original landed data |
| clean/silver | validated and standardized data |
| curated/gold | business-ready tables |
| archive | older retained data |

## 6. How It Works Step By Step

1. Create a bucket.
2. Store objects using keys, such as `raw/orders/dt=2026-07-01/file.parquet`.
3. Control access with IAM and bucket policies.
4. Encrypt data at rest.
5. Catalog data with Glue Data Catalog if needed.
6. Query with Athena, Spark, Redshift Spectrum, or other engines.
7. Use lifecycle rules to move/delete older data.

## 7. How To Use It Practically

Good data lake habits:

- use clear prefixes
- partition by common filters like date
- store curated analytics data in Parquet/ORC
- avoid millions of tiny files
- enable encryption
- use lifecycle policies
- restrict public access
- separate raw and curated zones

Example path:

```text
s3://company-data-lake/bronze/orders/dt=2026-07-01/part-0001.parquet
```

## 8. Real-World Scenario

- Product/system: E-commerce clickstream lake.
- Problem: Billions of raw click events must be stored cheaply for replay and analytics.
- How S3 helps: raw events land in S3, Spark/Glue cleans them, Athena/Redshift/ML jobs consume curated data.
- What would go wrong without structure: users cannot find data, costs rise, and queries scan too much.

## 9. System Design Angle

Use S3 when:

- data lake storage is needed
- raw immutable data must be retained
- multiple compute engines need shared data
- batch analytics and replay matter

Be careful with:

- IAM permissions
- public access
- small files
- partition design
- lifecycle/cost
- data catalog consistency

## 10. Trade-offs

| Pros | Cons |
|---|---|
| highly scalable storage | not a database by itself |
| works with many AWS services | object layout matters for performance |
| good for data lakes | small files hurt query engines |
| lifecycle/storage tiers | access/security must be designed |
| durable raw archive | eventual platform governance needed |

## 11. Failure Modes

- Failure: Wrong bucket policy.
- Symptom: unauthorized access or blocked jobs.
- Recovery: fix IAM/bucket policy.
- Prevention: least privilege and policy review.

- Failure: Too many tiny files.
- Symptom: Athena/Spark queries slow.
- Recovery: compact files.
- Prevention: batch writes and target file sizes.

- Failure: Poor partition layout.
- Symptom: queries scan too much data.
- Recovery: reorganize/rewrite curated tables.
- Prevention: design around query filters.

## 12. Common Mistakes

- Mistake: Treating S3 like a folder-based database.
- Why it is wrong: S3 stores objects; query behavior depends on engines/catalogs.
- Better approach: use table formats/catalogs and good layout.

- Mistake: Leaving raw data ungoverned.
- Why it is wrong: PII and sensitive data can spread.
- Better approach: classify, encrypt, restrict, and audit.

## 13. Mini Example

```text
Raw:
s3://lake/bronze/orders/json/...

Curated:
s3://lake/silver/orders_parquet/dt=2026-07-01/...

Gold:
s3://lake/gold/daily_revenue/...
```

## 14. Interview Questions

1. What is S3?
2. Why is S3 used for data lakes?
3. How do partitioning and file format affect Athena/Spark?
4. How do you secure S3 data?
5. What is the small files problem in S3?

## 15. Interview Speak

"S3 is the durable object storage foundation for many AWS data lakes. I would store raw immutable data, curate it into partitioned columnar formats, catalog it with Glue, query it through Athena/Spark/Redshift, and control security with IAM, encryption, lifecycle policies, and auditing."

## 16. Quick Recall

- One-line summary: S3 is AWS object storage for data lakes.
- Three keywords: bucket, object, data lake.
- One trap: Thinking S3 alone gives table transactions/query optimization.
- One memory trick: Cloud warehouse for objects.
