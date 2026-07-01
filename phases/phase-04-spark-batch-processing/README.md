# Phase 4: Spark And Batch Processing

Phase 4 teaches Apache Spark from baby steps to production/interview depth.

Spark matters because it became the dominant distributed processing engine for many batch analytics, ETL, SQL, and machine learning pipelines after classic MapReduce. The mental model is:

```text
write transformations -> Spark builds a plan -> cluster runs tasks in parallel -> data is read, shuffled, cached, joined, and written
```

## Topics

| # | Topic | Status |
|---:|---|---|
| 078 | Apache Spark overview | Complete |
| 079 | Spark architecture | Complete |
| 080 | Driver and executors | Complete |
| 081 | Spark cluster manager | Complete |
| 082 | RDD | Complete |
| 083 | DataFrame | Complete |
| 084 | Dataset | Complete |
| 085 | Transformations vs actions | Complete |
| 086 | Lazy evaluation | Complete |
| 087 | DAG | Complete |
| 088 | Stages and tasks | Complete |
| 089 | Narrow vs wide transformations | Complete |
| 090 | Shuffle | Complete |
| 091 | Broadcast join | Complete |
| 092 | Sort-merge join | Complete |
| 093 | Partitioning in Spark | Complete |
| 094 | Caching and persistence | Complete |
| 095 | Spark SQL | Complete |
| 096 | Catalyst optimizer | Complete |
| 097 | Tungsten engine | Complete |
| 098 | Adaptive query execution | Complete |
| 099 | Data skew | Complete |
| 100 | Small files problem | Complete |
| 101 | Spark memory management | Complete |
| 102 | Spark performance tuning | Complete |
| 103 | Spark job failure handling | Complete |
| 104 | PySpark | Complete |
| 105 | Spark on Kubernetes | Complete |
| 106 | Spark on EMR/Dataproc/Databricks | Complete |

## Phase Goal

By the end of this phase, you should be able to explain:

- why Spark became popular after MapReduce
- how Spark applications run across driver and executors
- what RDDs, DataFrames, and Datasets are
- why Spark is lazy
- how DAGs, stages, tasks, narrow/wide transformations, and shuffle work
- how joins, partitioning, caching, SQL, Catalyst, Tungsten, and AQE affect performance
- how to debug skew, small files, memory issues, and failed jobs
- how PySpark and deployment platforms fit into real data engineering work

## Suggested Study Flow

1. Read Topics 078-084 for Spark vocabulary.
2. Read Topics 085-094 for the execution model.
3. Read Topics 095-103 for SQL internals and performance.
4. Read Topics 104-106 for practical development and deployment.
5. Finish with `phase-04-review.md`.
