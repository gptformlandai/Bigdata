# Phase 6: Modern Data Lakehouse

Phase 6 teaches modern lakehouse systems from baby steps to production/interview depth.

The mental model is:

```text
cheap object storage holds data files
  -> table format tracks metadata, snapshots, schema, and commits
  -> engines like Spark, Flink, Trino, or Databricks read/write the table safely
```

A lakehouse tries to combine the low-cost, flexible storage of a data lake with important warehouse-like features: ACID transactions, schema control, upserts, time travel, performance tuning, and governance.

## Topics

| # | Topic | Status |
|---:|---|---|
| 138 | Data lakehouse architecture | Complete |
| 139 | Apache Iceberg | Complete |
| 140 | Delta Lake | Complete |
| 141 | Apache Hudi | Complete |
| 142 | Table formats | Complete |
| 143 | Snapshot isolation | Complete |
| 144 | Time travel | Complete |
| 145 | ACID on data lake | Complete |
| 146 | Compaction | Complete |
| 147 | Merge-on-read vs copy-on-write | Complete |
| 148 | Upserts on data lake | Complete |
| 149 | Metadata scaling | Complete |
| 150 | Partition evolution | Complete |
| 151 | Hidden partitioning | Complete |
| 152 | Z-ordering/clustering | Complete |
| 153 | Vacuum/cleanup | Complete |
| 154 | Lakehouse performance tuning | Complete |

## Phase Goal

By the end of this phase, you should be able to explain:

- why lakehouse architecture exists
- how object storage, file formats, table formats, catalogs, and query engines work together
- how Iceberg, Delta Lake, and Hudi are similar and different
- how snapshots, time travel, and ACID commits work on a data lake
- why compaction, cleanup, partition evolution, hidden partitioning, and clustering matter
- how to design and tune a lakehouse table for production workloads

## Suggested Study Flow

1. Read Topic 138 for the full lakehouse mental model.
2. Read Topics 139-142 to understand Iceberg, Delta, Hudi, and table formats.
3. Read Topics 143-145 to understand transactions, snapshots, and time travel.
4. Read Topics 146-148 for updates, deletes, and file rewrite strategies.
5. Read Topics 149-154 for production scaling and performance tuning.
6. Finish with `phase-06-review.md`.
