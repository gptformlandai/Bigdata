# Topic 208: Azure Data Lake Storage

## 1. Goal

Understand Azure Data Lake Storage as the object/data lake storage foundation on Azure.

## 2. Baby Intuition

ADLS is Azure's cloud storage home for big analytical files.

It is where raw, cleaned, and curated data lake files commonly live.

## 3. What It Is

- Simple definition: Azure Data Lake Storage stores data lake files on Azure.
- Technical definition: Azure Data Lake Storage is scalable cloud storage for analytics workloads, commonly used with hierarchical namespaces, access control, and integration with Azure analytics services.
- Category: Cloud data lake storage.
- Related terms: storage account, container, blob, hierarchical namespace, ACL, Synapse, Databricks, Event Hubs.

## 4. Why It Exists

Azure data platforms need durable storage for:

- raw events
- log files
- batch extracts
- lakehouse tables
- ML datasets
- archive data

ADLS provides the data lake storage layer that Synapse, Databricks, and other services can read/write.

## 5. Where It Fits In A Data Platform

```text
sources/events/files
  -> ADLS bronze/raw
  -> Synapse/Databricks/Data Factory transforms
  -> ADLS silver/gold or warehouse
  -> BI/ML/reporting
```

## 6. How It Works Step By Step

1. Create storage account and container.
2. Organize data by zones and prefixes/paths.
3. Configure identity, RBAC, and ACLs.
4. Encrypt data at rest.
5. Write raw data from pipelines/streams.
6. Process with Databricks/Synapse.
7. Serve curated data through SQL/BI/ML.

## 7. How To Use It Practically

Good lake layout:

```text
abfss://lake@account.dfs.core.windows.net/bronze/orders/dt=2026-07-01/
abfss://lake@account.dfs.core.windows.net/silver/orders/
abfss://lake@account.dfs.core.windows.net/gold/revenue_daily/
```

Good practices:

- separate raw/clean/curated zones
- use Parquet/Delta/Iceberg/Hudi where appropriate
- control access by zone
- avoid tiny files
- set lifecycle/retention rules
- audit access to sensitive data

## 8. Real-World Scenario

- Product/system: Healthcare analytics lake on Azure.
- Problem: Claims, member, and provider files need secure storage and processing.
- How ADLS helps: raw files land securely, transformations create curated Delta tables, Synapse/Power BI consume trusted outputs.
- What would go wrong without governance: sensitive data access becomes uncontrolled.

## 9. System Design Angle

Use ADLS when:

- Azure data lake storage is needed
- Databricks/Synapse will process lake data
- enterprise security and ACLs matter
- raw and curated zones are required

Be careful with:

- RBAC vs ACL complexity
- storage layout
- small files
- encryption/key management
- private networking

## 10. Trade-offs

| Pros | Cons |
|---|---|
| scalable lake storage | not a query engine by itself |
| integrates with Azure analytics | access design can be complex |
| supports hierarchical namespace patterns | layout matters |
| good for lakehouse tables | small files still hurt |

## 11. Failure Modes

- Failure: Wrong ACL/RBAC.
- Symptom: users/jobs cannot access data or over-access sensitive files.
- Recovery: fix permissions.
- Prevention: least privilege and access reviews.

- Failure: Poor zone separation.
- Symptom: raw data consumed as trusted data.
- Recovery: reorganize and restrict.
- Prevention: bronze/silver/gold standards.

- Failure: Too many small files.
- Symptom: slow Spark/Synapse queries.
- Recovery: compaction.
- Prevention: tuned writers.

## 12. Common Mistakes

- Mistake: Using one open container for all data.
- Why it is wrong: sensitive raw and curated trusted data need different controls.
- Better approach: zone data and permissions.

- Mistake: Thinking ADLS alone is a lakehouse.
- Why it is wrong: ADLS stores files; table/transaction behavior comes from formats and engines.
- Better approach: pair ADLS with Delta/Iceberg/Hudi and compute engines.

## 13. Mini Example

```text
Event Hubs
  -> stream writer
  -> ADLS bronze
  -> Azure Databricks Delta silver/gold
  -> Synapse/Power BI
```

## 14. Interview Questions

1. What is ADLS?
2. How does it fit in Azure data lake architecture?
3. How do Synapse and Databricks use ADLS?
4. How do you secure ADLS?
5. Why does file layout matter?

## 15. Interview Speak

"Azure Data Lake Storage is the scalable storage foundation for Azure data lakes. I would organize it into raw, clean, and curated zones, process it with Synapse or Databricks, use columnar/lakehouse formats, and secure it with RBAC, ACLs, encryption, private networking, and auditing."

## 16. Quick Recall

- One-line summary: ADLS is Azure's data lake storage layer.
- Three keywords: storage account, container, ACL.
- One trap: Treating storage alone as lakehouse.
- One memory trick: Azure lake file home.
