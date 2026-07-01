# Topic 211: Azure Databricks

## 1. Goal

Understand Azure Databricks as a managed Spark/lakehouse platform on Azure.

## 2. Baby Intuition

Azure Databricks is like a collaborative Spark and lakehouse workspace.

Data engineers, analysts, and ML teams use notebooks/jobs/clusters to process data in ADLS.

## 3. What It Is

- Simple definition: Azure Databricks is a managed Databricks platform integrated with Azure.
- Technical definition: Azure Databricks provides managed Apache Spark, notebooks, jobs, clusters, Delta Lake/lakehouse workflows, ML integrations, and Azure identity/storage integrations.
- Category: Managed Spark/lakehouse platform.
- Related terms: Spark, Delta Lake, cluster, job, notebook, ADLS, Unity Catalog, lakehouse.

## 4. Why It Exists

Teams need a productive platform for:

- Spark ETL
- lakehouse tables
- notebooks
- batch and streaming jobs
- ML feature/data pipelines
- Delta Lake workflows
- collaboration

Databricks packages these capabilities with managed infrastructure and developer tools.

## 5. Where It Fits In A Data Platform

```text
ADLS raw data
  -> Azure Databricks Spark/Delta pipelines
  -> ADLS lakehouse tables
  -> Synapse/Power BI/ML/serving
```

## 6. How It Works Step By Step

1. Data lands in ADLS.
2. Databricks cluster/job reads data.
3. Spark transforms, cleans, joins, and aggregates.
4. Delta/lakehouse tables store curated outputs.
5. Jobs/notebooks orchestrate recurring processing.
6. Downstream tools query outputs.
7. Governance, access, and monitoring control production use.

## 7. How To Use It Practically

Common uses:

| Use | Example |
|---|---|
| batch ETL | daily Spark transformations |
| streaming | Event Hubs to Delta tables |
| lakehouse | bronze/silver/gold Delta tables |
| ML | feature generation and training data |
| notebooks | exploration and collaboration |
| jobs | scheduled production workloads |

Good practices:

- keep production jobs version controlled
- use job clusters for cost isolation
- optimize Delta tables
- avoid all work in ad hoc notebooks
- use access controls and secret management

## 8. Real-World Scenario

- Product/system: Azure lakehouse.
- Problem: Raw orders, clicks, and customer events need bronze/silver/gold processing.
- How Azure Databricks helps: Spark reads ADLS bronze, writes Delta silver/gold, optimizes tables, and serves downstream BI/ML.
- What would go wrong without governance: notebooks become hidden production pipelines.

## 9. System Design Angle

Use Azure Databricks when:

- Spark/lakehouse workloads are central
- Delta Lake workflows matter
- notebooks/jobs collaboration is useful
- batch and streaming processing are both needed
- Azure storage/identity integration matters

Compare:

- Synapse for integrated SQL/Spark/PBI workspace
- Databricks for Spark/lakehouse/developer productivity
- ADLS as storage layer, not compute

## 10. Trade-offs

| Pros | Cons |
|---|---|
| strong Spark/lakehouse experience | cost governance needed |
| collaborative notebooks/jobs | notebook sprawl risk |
| Delta Lake integration | platform-specific workflow choices |
| batch and streaming | cluster tuning still matters |
| Azure integration | access/governance setup needed |

## 11. Failure Modes

- Failure: Cluster oversized/left running.
- Symptom: high cost.
- Recovery: terminate/resize.
- Prevention: job clusters, auto-termination, budgets.

- Failure: Notebook used as hidden production code.
- Symptom: no review/testing.
- Recovery: move to repos/jobs.
- Prevention: CI/CD and ownership.

- Failure: Poor table layout.
- Symptom: slow Delta/Spark queries.
- Recovery: optimize/compact/partition carefully.
- Prevention: table maintenance strategy.

## 12. Common Mistakes

- Mistake: Treating Databricks as only notebooks.
- Why it is wrong: production needs jobs, repos, tests, monitoring, and governance.
- Better approach: separate exploration from production pipelines.

- Mistake: Ignoring cluster cost.
- Why it is wrong: idle or oversized clusters can be expensive.
- Better approach: use auto-termination, job clusters, and right sizing.

## 13. Mini Example

```text
Event Hubs
  -> Databricks Structured Streaming
  -> ADLS bronze Delta
  -> silver cleaned table
  -> gold dashboard aggregate
```

## 14. Interview Questions

1. What is Azure Databricks?
2. How does it relate to Spark?
3. How does it use ADLS?
4. Databricks vs Synapse?
5. How do you control Databricks cost?

## 15. Interview Speak

"Azure Databricks is a managed Spark/lakehouse platform integrated with Azure. I would use it for batch and streaming Spark pipelines over ADLS, Delta Lake bronze/silver/gold tables, and ML/data engineering workflows, while managing cluster cost, CI/CD, governance, and table optimization."

## 16. Quick Recall

- One-line summary: Azure Databricks is managed Spark/lakehouse on Azure.
- Three keywords: Spark, Delta, ADLS.
- One trap: Ad hoc notebooks becoming production.
- One memory trick: Collaborative Spark lakehouse workspace.
