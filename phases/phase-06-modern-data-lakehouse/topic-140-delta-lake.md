# Topic 140: Delta Lake

## 1. Goal

Understand Delta Lake as a lakehouse table format built around a transaction log.

## 2. Baby Intuition

Delta Lake is like a shared spreadsheet with a changelog.

Every write records what was added, removed, or changed, so readers know the exact current version of the table.

## 3. What It Is

- Simple definition: Delta Lake is a table format/storage layer that adds transactions and table management to data lake files.
- Technical definition: Delta Lake stores data as Parquet files and tracks table changes in a `_delta_log` transaction log, enabling ACID transactions, schema enforcement/evolution, time travel, MERGE, and optimization features.
- Category: Lakehouse table format.
- Related terms: transaction log, version, checkpoint, MERGE, OPTIMIZE, ZORDER, Databricks, Spark.

## 4. Why It Exists

Plain data lakes had common problems:

- failed jobs left partial data
- concurrent writers could corrupt table state
- schema changes broke readers
- updates and deletes were hard
- old table versions were difficult to recover

Delta Lake exists to make data lake tables reliable and easy to use, especially in Spark-heavy lakehouse platforms.

## 5. Where It Fits In A Data Platform

```text
Spark/Databricks/Flink/other engines
  -> Delta table
  -> Parquet data files
  -> _delta_log transaction files
  -> object storage
```

The transaction log is the source of truth for the table.

## 6. How It Works Step By Step

1. Data files are written as Parquet.
2. The writer records actions in `_delta_log`.
3. Actions describe added files, removed files, metadata, protocol versions, and commits.
4. A successful commit creates a new table version.
5. Readers reconstruct the table state from the log and checkpoints.
6. Time travel reads older versions.
7. VACUUM can remove old files after the retention period.

Mental model:

```text
data files = physical data
_delta_log = official table history
```

## 7. How To Use It Practically

Common operations:

```sql
CREATE TABLE orders USING DELTA AS
SELECT * FROM raw_orders;

MERGE INTO orders target
USING order_updates source
ON target.order_id = source.order_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

OPTIMIZE orders;
```

Delta is commonly used with:

- Databricks lakehouse
- Spark batch pipelines
- structured streaming sinks
- CDC merge pipelines
- BI and ML tables

## 8. Real-World Scenario

- Product/system: Customer 360 table.
- Problem: Customer records change frequently and downstream dashboards need reliable current data.
- How Delta helps: Use MERGE for upserts, schema enforcement for safety, time travel for debugging, and OPTIMIZE for query speed.
- What would go wrong without it: manual rewrites become risky and failed jobs may expose partial data.

## 9. System Design Angle

Use Delta Lake when:

- your platform is Spark/Databricks-heavy
- you need ACID, MERGE, streaming writes, and time travel
- teams want simple operational commands like OPTIMIZE and VACUUM
- you need reliable bronze/silver/gold pipelines

Be careful with:

- retention settings
- VACUUM timing
- small file growth
- feature compatibility across non-Databricks engines

## 10. Trade-offs

| Pros | Cons |
|---|---|
| strong Spark/Databricks integration | not every engine supports every feature |
| simple transaction log model | log/checkpoint maintenance matters |
| good MERGE support | updates may rewrite files |
| time travel | old versions cost storage |
| optimization commands | operational tuning still needed |

## 11. Failure Modes

- Failure: VACUUM removes files still needed by a long-running reader.
- Symptom: reader fails because old files are gone.
- Recovery: rerun query on valid version.
- Prevention: set safe retention windows.

- Failure: Many tiny streaming output files.
- Symptom: slow queries.
- Recovery: OPTIMIZE/compaction.
- Prevention: tune trigger intervals and file size.

- Failure: Bad schema change.
- Symptom: writes fail or readers break.
- Recovery: rollback/time travel if possible.
- Prevention: schema governance and test pipelines.

## 12. Common Mistakes

- Mistake: Manually editing `_delta_log`.
- Why it is wrong: it can corrupt table history.
- Better approach: use Delta commands/APIs.

- Mistake: Running VACUUM aggressively.
- Why it is wrong: it can break time travel and active readers.
- Better approach: choose retention based on SLA and audit needs.

## 13. Mini Example

```text
Version 0: create table with files A, B
Version 1: MERGE adds C and removes B
Current table: A, C
Time travel to version 0: A, B
```

## 14. Interview Questions

1. What is Delta Lake?
2. What is `_delta_log`?
3. How does Delta support time travel?
4. How does MERGE work at a high level?
5. What does VACUUM do?

## 15. Interview Speak

"Delta Lake adds a transaction log on top of Parquet data files in object storage. The log tracks table versions and file add/remove actions, enabling ACID transactions, time travel, schema enforcement, streaming/batch writes, and MERGE-based upserts."

## 16. Quick Recall

- One-line summary: Delta Lake is Parquet plus a transaction log.
- Three keywords: `_delta_log`, MERGE, time travel.
- One trap: Vacuuming before old readers/time travel are safe.
- One memory trick: Delta keeps the table diary.
