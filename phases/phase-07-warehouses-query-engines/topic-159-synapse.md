# Topic 159: Synapse

## 1. Goal

Understand Azure Synapse Analytics as Microsoft's analytics platform for warehouses, lake queries, and pipelines.

## 2. Baby Intuition

Synapse is like an Azure analytics workshop.

It can run warehouse SQL, query lake files, connect pipelines, and integrate with Microsoft BI tools.

## 3. What It Is

- Simple definition: Synapse is Azure's analytics platform for warehousing and big data querying.
- Technical definition: Azure Synapse Analytics combines data warehousing, SQL query, Spark integration, data integration, and lake analytics capabilities in the Azure ecosystem.
- Category: Cloud analytics platform.
- Related terms: dedicated SQL pool, serverless SQL pool, Spark pool, Data Lake Storage, Power BI, distribution, CTAS.

## 4. Why It Exists

Organizations on Azure need a unified way to:

- load and transform data
- query warehouse tables
- query files in a data lake
- run Spark jobs
- serve Power BI dashboards
- govern enterprise data

Synapse packages these analytics capabilities around Azure services.

## 5. Where It Fits In A Data Platform

```text
Azure sources / ADLS / Event Hubs / databases
  -> Synapse pipelines/Spark/SQL
  -> dedicated warehouse tables or lake queries
  -> Power BI / reports / analysts
```

## 6. How It Works Step By Step

Common dedicated SQL warehouse flow:

1. Data lands in Azure Data Lake Storage.
2. Pipeline or Spark job prepares data.
3. Data is loaded into dedicated SQL pool tables.
4. Tables are distributed for MPP processing.
5. Users run SQL queries.
6. Results feed Power BI or downstream consumers.

Serverless SQL flow:

1. Files stay in the lake.
2. SQL engine queries files directly.
3. Useful for exploration and lake queries.

## 7. How To Use It Practically

Important concepts:

| Concept | Meaning |
|---|---|
| dedicated SQL pool | provisioned warehouse compute |
| serverless SQL pool | query lake files without dedicated warehouse |
| Spark pool | Spark execution in Synapse |
| distribution | how table rows are spread |
| Power BI integration | dashboard/report serving |

## 8. Real-World Scenario

- Product/system: Enterprise reporting on Azure.
- Problem: Data lives in SQL Server, SaaS tools, and ADLS files.
- How Synapse helps: pipelines ingest data, SQL pools model data, serverless SQL explores lake files, Power BI serves dashboards.
- What would go wrong without planning: teams may mix workloads without cost/resource controls.

## 9. System Design Angle

Use Synapse when:

- Azure is the main cloud
- Microsoft ecosystem matters
- Power BI integration is central
- both warehouse and lake queries are needed
- enterprise governance is important

Be careful with:

- dedicated vs serverless cost model
- table distribution
- data movement
- workload isolation
- security across ADLS and SQL

## 10. Trade-offs

| Pros | Cons |
|---|---|
| strong Azure integration | platform complexity |
| warehouse plus lake query options | cost model depends on mode |
| Power BI ecosystem fit | tuning still required |
| Spark and SQL in one platform | users need clear workload guidance |

## 11. Failure Modes

- Failure: Wrong compute mode for workload.
- Symptom: unnecessary cost or poor performance.
- Recovery: move workload to better pool/mode.
- Prevention: classify workloads first.

- Failure: Poor table distribution.
- Symptom: slow joins and data movement.
- Recovery: redesign distribution.
- Prevention: model based on join/query patterns.

- Failure: Lake permissions mismatch.
- Symptom: SQL/Spark users cannot read files.
- Recovery: fix Azure roles/ACLs.
- Prevention: centralized access design.

## 12. Common Mistakes

- Mistake: Treating Synapse as only one thing.
- Why it is wrong: it includes multiple execution modes.
- Better approach: choose dedicated SQL, serverless SQL, or Spark based on workload.

- Mistake: Putting every workload on dedicated SQL.
- Why it is wrong: some exploration/lake reads may fit serverless better.
- Better approach: route workloads intentionally.

## 13. Mini Example

```text
Exploration:
serverless SQL queries CSV/Parquet in ADLS

Repeated BI:
dedicated SQL pool stores modeled fact/dim tables

Heavy transforms:
Spark pool processes large files
```

## 14. Interview Questions

1. What is Synapse?
2. Dedicated SQL pool vs serverless SQL pool?
3. Where does Spark fit?
4. How does Synapse work with ADLS?
5. What tuning issues matter?

## 15. Interview Speak

"Synapse is Azure's analytics platform that includes dedicated SQL warehouses, serverless SQL over lake files, Spark pools, and pipeline integration. I would choose the mode based on workload: dedicated SQL for repeated warehouse BI, serverless SQL for lake exploration, and Spark for large transformations."

## 16. Quick Recall

- One-line summary: Synapse is Azure's combined warehouse, lake query, and analytics workspace.
- Three keywords: dedicated SQL, serverless SQL, ADLS.
- One trap: Using the wrong compute mode for the workload.
- One memory trick: Azure analytics workshop.
