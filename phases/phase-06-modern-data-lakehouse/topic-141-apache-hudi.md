# Topic 141: Apache Hudi

## 1. Goal

Understand Apache Hudi as a lakehouse table format focused strongly on upserts and incremental data processing.

## 2. Baby Intuition

Hudi is like a notebook designed for corrections.

If a customer record changes, Hudi helps update the existing logical row instead of only appending endless duplicates.

## 3. What It Is

- Simple definition: Apache Hudi is a table format for data lakes that supports inserts, updates, deletes, and incremental queries.
- Technical definition: Hudi manages datasets using timelines, commits, file groups, record keys, indexing, and copy-on-write or merge-on-read storage modes to support efficient upserts and incremental processing.
- Category: Lakehouse table format.
- Related terms: record key, precombine field, timeline, commit, file group, copy-on-write, merge-on-read, CDC.

## 4. Why It Exists

Many data lake workloads are not pure append-only.

Real systems need:

- update customer records
- delete privacy-sensitive rows
- process CDC from databases
- deduplicate late events
- incrementally consume changed data

Hudi was built to make mutable lake datasets practical.

## 5. Where It Fits In A Data Platform

```text
Database CDC / events / batch files
  -> Spark/Flink Hudi writer
  -> Hudi table on object storage
  -> Spark/Trino/Presto/Hive queries
```

Hudi is common in pipelines where records change frequently.

## 6. How It Works Step By Step

1. Each record has a record key.
2. Incoming data may contain new rows or updates to existing rows.
3. Hudi uses an index to locate where existing records live.
4. The writer creates a new commit on the table timeline.
5. In copy-on-write mode, updated files are rewritten.
6. In merge-on-read mode, changes may be written to log/delta files first.
7. Readers use the timeline to see the correct table state.
8. Incremental queries can read only changes after a commit.

Important terms:

| Term | Meaning |
|---|---|
| record key | unique row identifier |
| precombine field | field used to pick latest version of duplicates |
| commit timeline | ordered history of table actions |
| file group | related base/log files for a slice of data |

## 7. How To Use It Practically

Common CDC pattern:

```text
MySQL binlog -> Kafka -> Spark/Flink -> Hudi upsert table -> analytics queries
```

Hudi write decisions:

- choose record key carefully
- choose precombine timestamp/version field
- decide copy-on-write vs merge-on-read
- plan compaction if using merge-on-read
- monitor clustering, file sizes, and commit timeline

## 8. Real-World Scenario

- Product/system: User profile lake table.
- Problem: Profiles change frequently and analytics need the latest value plus history.
- How Hudi helps: It handles record-key upserts, deduplication, incremental pulls, and storage modes optimized for update-heavy workloads.
- What would go wrong without it: append-only files would create many duplicate versions and every query would need complex latest-record logic.

## 9. System Design Angle

Use Hudi when:

- CDC/upserts are central
- incremental processing is important
- updates are frequent compared with pure append tables
- you need COW/MOR flexibility

Be careful with:

- index choice
- compaction scheduling
- write amplification
- query engine support
- record key correctness

## 10. Trade-offs

| Pros | Cons |
|---|---|
| strong upsert/CDC support | more concepts to configure |
| incremental queries | indexing overhead |
| COW and MOR modes | compaction can be required |
| dedupe support | bad keys cause bad tables |
| good for mutable datasets | pure append workloads may not need it |

## 11. Failure Modes

- Failure: Wrong record key.
- Symptom: duplicates or overwritten wrong rows.
- Recovery: rebuild table from source.
- Prevention: validate key uniqueness.

- Failure: Missing compaction for MOR table.
- Symptom: reads become slower.
- Recovery: run compaction.
- Prevention: schedule compaction based on query SLA.

- Failure: Bad precombine field.
- Symptom: older update wins over newer update.
- Recovery: replay CDC with correct ordering.
- Prevention: use reliable event timestamp/version.

## 12. Common Mistakes

- Mistake: Using Hudi without understanding keys.
- Why it is wrong: upsert quality depends on record identity.
- Better approach: define and test record key plus precombine field first.

- Mistake: Choosing MOR only for faster writes.
- Why it is wrong: read cost and compaction need planning.
- Better approach: choose COW or MOR based on read/write SLA.

## 13. Mini Example

```text
Incoming:
user_id=7, city=Austin, version=1
user_id=7, city=Dallas, version=2

Hudi keeps logical latest row:
user_id=7, city=Dallas
```

## 14. Interview Questions

1. What is Apache Hudi?
2. Why is Hudi useful for CDC?
3. What are record key and precombine field?
4. Compare copy-on-write and merge-on-read.
5. What are incremental queries?

## 15. Interview Speak

"Hudi is a lakehouse table format designed for mutable data. It supports upserts, deletes, incremental queries, and CDC-style ingestion using record keys, commit timelines, indexes, and either copy-on-write or merge-on-read storage modes."

## 16. Quick Recall

- One-line summary: Hudi is the upsert-friendly lakehouse table format.
- Three keywords: record key, timeline, upsert.
- One trap: Bad record keys silently damage correctness.
- One memory trick: Hudi is built for changing rows.
