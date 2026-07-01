# Topic 209: Azure Synapse

## 1. Goal

Understand Azure Synapse as Azure's integrated analytics platform.

## 2. Baby Intuition

Synapse is like an Azure analytics workspace.

It brings SQL warehousing, lake querying, Spark, and pipelines into one platform experience.

## 3. What It Is

- Simple definition: Synapse is Azure's analytics platform for warehouses, lake queries, and big data.
- Technical definition: Azure Synapse Analytics combines dedicated SQL pools, serverless SQL pools, Spark pools, data integration, and lake/warehouse analytics in the Azure ecosystem.
- Category: Cloud analytics platform.
- Related terms: dedicated SQL pool, serverless SQL pool, Spark pool, ADLS, Power BI, MPP, Data Factory.

## 4. Why It Exists

Azure data teams need to:

- query warehouse tables
- query files in ADLS
- transform big data
- integrate with Power BI
- build enterprise reporting
- combine SQL and Spark workflows

Synapse gives multiple analytics modes in one Azure platform.

## 5. Where It Fits In A Data Platform

```text
ADLS / databases / Event Hubs / SaaS
  -> Synapse pipelines, Spark, SQL
  -> warehouse tables or lake tables
  -> Power BI / analysts / reports
```

## 6. How It Works Step By Step

Dedicated warehouse pattern:

1. Data lands in ADLS.
2. Pipeline/Spark prepares data.
3. Data loads into dedicated SQL pool.
4. Users query modeled warehouse tables.
5. Power BI serves dashboards.

Serverless lake query pattern:

1. Data remains in ADLS.
2. Serverless SQL queries files/tables.
3. Useful for exploration and lake analytics.

## 7. How To Use It Practically

Choose mode by workload:

| Mode | Use |
|---|---|
| dedicated SQL pool | repeated warehouse BI |
| serverless SQL pool | ad hoc lake file queries |
| Spark pool | big data transformations |
| pipelines | orchestration/ingestion |
| Power BI integration | dashboards |

## 8. Real-World Scenario

- Product/system: Enterprise finance reporting on Azure.
- Problem: Finance needs governed BI while data engineers process lake files.
- How Synapse helps: Spark/SQL transforms ADLS data, dedicated SQL serves repeated reporting, Power BI consumes curated outputs.
- What would go wrong without workload separation: exploration jobs can interfere with critical BI.

## 9. System Design Angle

Use Synapse when:

- Azure ecosystem is central
- Power BI integration matters
- both lake and warehouse workloads exist
- SQL and Spark users need shared workspace

Be careful with:

- choosing dedicated vs serverless SQL
- distribution/table design
- cost controls
- permissions across ADLS and SQL
- workload isolation

## 10. Trade-offs

| Pros | Cons |
|---|---|
| integrated Azure analytics | many modes to understand |
| SQL and Spark support | cost/performance varies by mode |
| Power BI fit | tuning still needed |
| ADLS integration | security model needs planning |

## 11. Failure Modes

- Failure: Wrong compute mode.
- Symptom: slow or expensive workload.
- Recovery: move to better mode.
- Prevention: workload classification.

- Failure: Poor distribution in dedicated SQL.
- Symptom: slow joins.
- Recovery: redesign distribution.
- Prevention: model based on query patterns.

- Failure: ADLS permission issue.
- Symptom: Synapse cannot read/write lake data.
- Recovery: fix identity/ACL/RBAC.
- Prevention: access tests.

## 12. Common Mistakes

- Mistake: Treating Synapse as only a warehouse.
- Why it is wrong: it includes SQL, Spark, lake query, and integration capabilities.
- Better approach: choose the right capability per workload.

- Mistake: Using serverless SQL for every repeated dashboard.
- Why it is wrong: repeated heavy BI may need modeled/optimized storage.
- Better approach: create marts/materialized outputs where needed.

## 13. Mini Example

```text
ADLS bronze files
  -> Synapse Spark cleans data
  -> dedicated SQL pool stores sales mart
  -> Power BI dashboard
```

## 14. Interview Questions

1. What is Azure Synapse?
2. Dedicated SQL vs serverless SQL?
3. Where does Spark fit?
4. Synapse vs Azure Databricks?
5. How do you control Synapse cost?

## 15. Interview Speak

"Azure Synapse is an integrated Azure analytics platform with dedicated SQL warehousing, serverless SQL over lake files, Spark pools, and pipeline integration. I would choose the execution mode based on workload and manage cost, security, table design, and ADLS access carefully."

## 16. Quick Recall

- One-line summary: Synapse is Azure's SQL, Spark, lake, and BI analytics workspace.
- Three keywords: dedicated SQL, serverless SQL, Spark.
- One trap: Wrong compute mode.
- One memory trick: Azure analytics workshop.
