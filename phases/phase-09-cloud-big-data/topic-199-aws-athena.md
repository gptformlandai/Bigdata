# Topic 199: AWS Athena

## 1. Goal

Understand AWS Athena as serverless SQL over data in S3.

## 2. Baby Intuition

Athena lets you ask SQL questions directly over files in S3.

You do not load data into a warehouse first for many ad hoc lake queries.

## 3. What It Is

- Simple definition: Athena is AWS serverless SQL for S3 data.
- Technical definition: Amazon Athena is a managed query service that uses catalog metadata to run SQL queries over data stored in S3 and supported table/file formats.
- Category: Serverless lake query service.
- Related terms: S3, Glue Data Catalog, external table, partition, Parquet, query scan, Athena engine.

## 4. Why It Exists

Data lakes need easy exploration.

Athena helps teams:

- query S3 data with SQL
- validate data lake files
- run ad hoc analytics
- avoid provisioning clusters for small/medium SQL use cases
- integrate with Glue Data Catalog

## 5. Where It Fits In A Data Platform

```text
S3 curated data
  -> Glue Data Catalog table
  -> Athena SQL query
  -> analyst/BI/ad hoc validation
```

Athena is query compute. S3 is storage. Glue Catalog is metadata.

## 6. How It Works Step By Step

1. Data files are stored in S3.
2. Table schema/partitions are registered in Glue Data Catalog.
3. User runs SQL in Athena.
4. Athena plans the query using catalog metadata.
5. Athena scans matching S3 files.
6. Results are returned or written to S3.

## 7. How To Use It Practically

Good practices:

- use Parquet/ORC for curated data
- partition by common filters
- avoid tiny files
- avoid `SELECT *`
- compress data
- keep catalog partitions up to date
- monitor scanned bytes/cost

Example:

```sql
SELECT event_type, COUNT(*)
FROM lake.events
WHERE event_date = DATE '2026-07-01'
GROUP BY event_type;
```

## 8. Real-World Scenario

- Product/system: Security log lake.
- Problem: Security team needs SQL over logs stored in S3.
- How Athena helps: external tables expose logs as SQL tables without loading them into Redshift first.
- What would go wrong without layout: raw JSON and no partitions make queries slow and costly.

## 9. System Design Angle

Use Athena when:

- data is already in S3
- query workload is ad hoc or moderate
- serverless SQL is useful
- open table/file formats are used

Avoid as primary engine when:

- sub-second serving is required
- high concurrency dashboards need predictable latency
- repeated heavy transformations should be materialized elsewhere

## 10. Trade-offs

| Pros | Cons |
|---|---|
| serverless | depends heavily on S3 layout |
| no loading needed | repeated full scans cost money |
| good for ad hoc SQL | not low-latency serving DB |
| integrates with Glue | small files hurt |
| works with open data | catalog maintenance needed |

## 11. Failure Modes

- Failure: Missing partition metadata.
- Symptom: query misses data.
- Recovery: repair/update catalog partitions.
- Prevention: automated partition registration.

- Failure: Query scans too much.
- Symptom: slow/high cost.
- Recovery: add filters, partitioning, Parquet.
- Prevention: table design standards.

- Failure: S3 permission issue.
- Symptom: query fails access denied.
- Recovery: fix IAM.
- Prevention: tested access roles.

## 12. Common Mistakes

- Mistake: Querying raw CSV forever.
- Why it is wrong: text files scan and parse more data.
- Better approach: convert curated datasets to Parquet/ORC.

- Mistake: Using Athena like an API backend.
- Why it is wrong: it is not meant for high-QPS low-latency serving.
- Better approach: use a warehouse/OLAP serving store/cache.

## 13. Mini Example

```text
S3:
events/event_date=2026-07-01/part-0001.parquet

Glue:
table events partitioned by event_date

Athena:
SQL scans only matching date partition
```

## 14. Interview Questions

1. What is Athena?
2. How does Athena relate to S3 and Glue?
3. How do you reduce Athena query cost?
4. Athena vs Redshift?
5. What file formats work best for analytics?

## 15. Interview Speak

"Athena is serverless SQL over S3 using Glue Catalog metadata. It is good for ad hoc lake queries and validation, but performance and cost depend on partitioning, columnar formats, compression, and file size. For repeated BI, I may materialize data into Redshift or an aggregate store."

## 16. Quick Recall

- One-line summary: Athena runs SQL over S3 files.
- Three keywords: S3, Glue, serverless SQL.
- One trap: Unpartitioned raw file scans.
- One memory trick: SQL flashlight over S3.
