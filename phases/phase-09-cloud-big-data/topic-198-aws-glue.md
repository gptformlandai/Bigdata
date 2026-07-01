# Topic 198: AWS Glue

## 1. Goal

Understand AWS Glue as a serverless data integration and catalog service.

## 2. Baby Intuition

Glue helps connect data pieces together.

It can catalog where data is, infer schemas, and run ETL jobs without you managing a Spark cluster directly.

## 3. What It Is

- Simple definition: Glue is AWS's managed data catalog and ETL service.
- Technical definition: AWS Glue provides a Data Catalog, crawlers, ETL jobs, schema discovery, and serverless data integration capabilities commonly used with S3 data lakes and analytics services.
- Category: Serverless data integration and metadata.
- Related terms: Glue Data Catalog, crawler, job, database, table, schema, ETL, Spark.

## 4. Why It Exists

Data lakes need:

- metadata/catalog tables
- schema discovery
- ETL jobs
- integration with Athena/EMR/Redshift
- serverless transformations

Without cataloging, files in S3 are hard to query and govern.

## 5. Where It Fits In A Data Platform

```text
S3 raw files
  -> Glue crawler/catalog
  -> Glue ETL job transforms data
  -> S3 curated tables
  -> Athena/Redshift/EMR query
```

Glue Data Catalog often acts as the shared metastore for AWS analytics.

## 6. How It Works Step By Step

1. Data lands in S3 or another source.
2. Crawler can inspect files and infer schema.
3. Glue Data Catalog stores database/table metadata.
4. Glue job reads source data.
5. Job transforms/cleans data.
6. Output is written to S3/warehouse/target.
7. Downstream services query cataloged tables.

## 7. How To Use It Practically

Common uses:

| Glue Feature | Use |
|---|---|
| Data Catalog | central table/schema metadata |
| crawler | infer schemas from files |
| ETL job | transform data serverlessly |
| workflow | coordinate related Glue jobs |
| schema registry | govern streaming schemas in some patterns |

Practical advice:

- do not rely blindly on crawlers for critical schemas
- version/control important schemas
- store curated data as Parquet
- partition large datasets
- monitor job duration/cost

## 8. Real-World Scenario

- Product/system: S3 sales data lake.
- Problem: Analysts need Athena SQL over daily sales files.
- How Glue helps: crawler/catalog registers table metadata; Glue job converts raw CSV to curated Parquet.
- What would go wrong without it: Athena users manually define schemas and query messy raw files.

## 9. System Design Angle

Use Glue when:

- AWS-native serverless ETL is useful
- S3 data needs catalog metadata
- Athena/EMR/Redshift need shared table definitions
- jobs are Spark-like transformations without cluster management

Be careful with:

- schema drift
- crawler mistakes
- job startup/runtime cost
- complex Spark tuning
- IAM role permissions

## 10. Trade-offs

| Pros | Cons |
|---|---|
| serverless ETL | less cluster-level control than EMR |
| central Data Catalog | crawler inference can be wrong |
| integrates with Athena/S3 | job debugging still needed |
| reduces operations | cost depends on job usage |
| supports common ETL patterns | complex workloads may need EMR/Databricks |

## 11. Failure Modes

- Failure: Crawler infers wrong schema.
- Symptom: query errors or wrong types.
- Recovery: update schema manually.
- Prevention: schema contracts and controlled catalog changes.

- Failure: Glue job fails on bad records.
- Symptom: ETL run fails.
- Recovery: quarantine bad data and rerun.
- Prevention: validation and dead-letter paths.

- Failure: IAM role missing S3 permissions.
- Symptom: job cannot read/write.
- Recovery: update role.
- Prevention: least-privilege role tests.

## 12. Common Mistakes

- Mistake: Treating crawlers as governance.
- Why it is wrong: schema inference is not the same as a data contract.
- Better approach: validate and control important schemas.

- Mistake: Using Glue for every transformation automatically.
- Why it is wrong: some workloads fit dbt, Athena, EMR, Lambda, or warehouse SQL better.
- Better approach: choose by workload size, latency, complexity, and cost.

## 13. Mini Example

```text
raw CSV in S3
  -> Glue crawler creates table metadata
  -> Glue job converts to partitioned Parquet
  -> Athena queries curated table
```

## 14. Interview Questions

1. What is AWS Glue?
2. What is Glue Data Catalog?
3. What does a crawler do?
4. Glue vs EMR?
5. How do you handle schema drift?

## 15. Interview Speak

"AWS Glue provides a serverless Data Catalog and ETL jobs for AWS data lakes. I would use the catalog as shared metadata for S3 tables and Athena/EMR, and use Glue jobs for managed transformations, while controlling schemas, IAM, partitioning, and data quality."

## 16. Quick Recall

- One-line summary: Glue catalogs and transforms AWS data lake data.
- Three keywords: catalog, crawler, ETL.
- One trap: Trusting crawler inference blindly.
- One memory trick: Glue gives files a table map.
