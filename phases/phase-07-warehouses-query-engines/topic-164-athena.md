# Topic 164: Athena

## 1. Goal

Understand Amazon Athena as a serverless SQL query service for data in S3.

## 2. Baby Intuition

Athena is like asking SQL questions directly over files in S3.

You do not start a warehouse cluster first; you define tables and query the lake.

## 3. What It Is

- Simple definition: Athena is serverless SQL over data in Amazon S3.
- Technical definition: Amazon Athena is a managed query service that uses SQL to analyze data in S3 through table metadata/catalogs and supported file/table formats.
- Category: Serverless lake query engine.
- Related terms: S3, Glue Data Catalog, external table, partition, Parquet, Iceberg, Presto/Trino lineage.

## 4. Why It Exists

Data lakes store huge amounts of data in S3.

Athena exists so users can:

- query files without loading into a warehouse first
- explore raw/curated lake data
- pay per query/scan pattern depending on setup
- integrate with AWS Glue catalog
- use SQL on open file formats

## 5. Where It Fits In A Data Platform

```text
S3 data lake
  -> Glue Data Catalog tables
  -> Athena SQL
  -> analysts, BI, validation, ad hoc reports
```

Athena is common for exploration, validation, and lightweight lake analytics.

## 6. How It Works Step By Step

1. Data files live in S3.
2. Table metadata is defined in a catalog.
3. User submits SQL to Athena.
4. Athena reads table metadata and partitions.
5. It scans required files from S3.
6. It processes SQL and writes/returns results.
7. Query performance depends heavily on file format and partitioning.

## 7. How To Use It Practically

Good practices:

- use Parquet/ORC instead of raw CSV when possible
- partition by common filters like date
- avoid too many tiny files
- select only needed columns
- keep table metadata updated
- use compressed columnar data

Example:

```sql
SELECT event_type, COUNT(*)
FROM lake.events
WHERE event_date = DATE '2026-07-01'
GROUP BY event_type;
```

## 8. Real-World Scenario

- Product/system: S3 audit log analysis.
- Problem: Security team needs ad hoc SQL on logs stored in S3.
- How Athena helps: define external tables and query logs without moving them into a warehouse.
- What would go wrong without tuning: raw JSON/CSV and missing partitions make scans slow and expensive.

## 9. System Design Angle

Use Athena when:

- data is already in S3
- query frequency is moderate/ad hoc
- serverless simplicity matters
- open file formats are used
- AWS Glue catalog is available

Avoid as primary serving layer when:

- sub-second dashboard latency is required
- query concurrency is very high
- workload needs heavy repeated transformations
- data layout is poor and cannot be fixed

## 10. Trade-offs

| Pros | Cons |
|---|---|
| serverless | performance depends on S3 layout |
| no data loading required | repeated queries can be costly |
| good for ad hoc lake SQL | not ideal for low-latency serving |
| works with open formats | small files hurt |
| AWS-native | catalog/partition maintenance needed |

## 11. Failure Modes

- Failure: Query scans unpartitioned raw files.
- Symptom: slow query and high cost.
- Recovery: convert to Parquet and partition.
- Prevention: lake table design standards.

- Failure: Partitions not registered.
- Symptom: query misses data.
- Recovery: repair/update catalog.
- Prevention: automated partition/catalog updates.

- Failure: Too many small files.
- Symptom: planning and scan overhead.
- Recovery: compact files.
- Prevention: batch writes and target file sizes.

## 12. Common Mistakes

- Mistake: Querying raw CSV forever.
- Why it is wrong: CSV scans unnecessary bytes and parses slowly.
- Better approach: convert curated datasets to Parquet/ORC.

- Mistake: Using Athena for high-QPS product APIs.
- Why it is wrong: it is not designed as a low-latency serving database.
- Better approach: use Pinot/Druid/ClickHouse/warehouse aggregate serving.

## 13. Mini Example

```text
Bad lake query:
S3 folder with 1 million tiny JSON files

Better:
partitioned Parquet files around hundreds of MB
cataloged by date
```

## 14. Interview Questions

1. What is Athena?
2. How does Athena query S3?
3. Why are Parquet and partitioning important?
4. Athena vs Redshift?
5. When should Athena not be used?

## 15. Interview Speak

"Athena is serverless SQL over data in S3 using catalog metadata. It is good for ad hoc lake analytics and validation, but performance and cost depend on file format, partitioning, compression, and file sizes. For repeated high-concurrency BI, I may use a warehouse or serving OLAP store."

## 16. Quick Recall

- One-line summary: Athena runs serverless SQL over S3 data.
- Three keywords: S3, Glue catalog, Parquet.
- One trap: Using raw unpartitioned files.
- One memory trick: SQL flashlight over S3.
