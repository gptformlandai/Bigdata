# Topic 148: Upserts On Data Lake

## 1. Goal

Understand how lakehouse systems support update-or-insert workloads on file-based storage.

## 2. Baby Intuition

An upsert says:

```text
If the row already exists, update it.
If it does not exist, insert it.
```

It is like updating a contact list: change the phone number if the person exists, otherwise add a new contact.

## 3. What It Is

- Simple definition: Upsert means update existing rows and insert new rows in one operation.
- Technical definition: A data lake upsert matches incoming records to existing table records using keys, then rewrites affected files or records changes through table-format metadata/logs.
- Category: Mutable lakehouse data operation.
- Related terms: MERGE, CDC, primary key, deduplication, record key, copy-on-write, merge-on-read.

## 4. Why It Exists

Many analytical tables need current state:

- customer profile
- account balance
- product catalog
- order status
- inventory level
- user consent/PII flags

Append-only data creates duplicates:

```text
user_id=1, city=Austin
user_id=1, city=Dallas
```

An upsert table keeps the logical current row.

## 5. Where It Fits In A Data Platform

```text
OLTP database
  -> CDC events
  -> Kafka
  -> Spark/Flink
  -> lakehouse MERGE/upsert table
  -> analytics/BI/ML
```

Upserts are common in silver tables and current-state dimension tables.

## 6. How It Works Step By Step

1. Incoming records contain a key.
2. The writer identifies matching existing records.
3. For matched keys, it updates/deletes/replaces records.
4. For unmatched keys, it inserts new records.
5. The table format writes new files or change logs.
6. The table commits a new snapshot/version.
7. Readers see the updated logical table.

High-level SQL:

```sql
MERGE INTO customers target
USING customer_updates source
ON target.customer_id = source.customer_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

## 7. How To Use It Practically

Design decisions:

- choose stable business key
- deduplicate source updates
- use event time/version to pick latest record
- handle deletes/tombstones
- batch updates to avoid tiny files
- monitor update rate and rewrite cost
- compact regularly

## 8. Real-World Scenario

- Product/system: Product catalog lakehouse table.
- Problem: Product price and availability change all day.
- How upserts help: Latest product state is maintained in one table for analytics/search/ML.
- What would go wrong without it: downstream queries must filter duplicate historical records every time.

## 9. System Design Angle

Clarify:

- What is the key?
- Are updates ordered?
- Can events arrive late?
- Are deletes required?
- Is history required or only latest state?
- What is the update volume?
- What is the read SLA?

Design pattern:

```text
bronze append-only CDC log
  -> silver current-state MERGE table
  -> gold aggregates/history
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| current-state table | more expensive than append-only |
| simpler downstream queries | needs reliable keys |
| supports CDC | file rewrites/logs required |
| handles deletes | compaction and cleanup needed |

## 11. Failure Modes

- Failure: Duplicate updates.
- Symptom: wrong latest row or unnecessary rewrites.
- Recovery: deduplicate and replay.
- Prevention: idempotent processing and version field.

- Failure: Out-of-order CDC events.
- Symptom: old value overwrites new value.
- Recovery: replay with correct ordering/version.
- Prevention: precombine/event version logic.

- Failure: High update rate with large files.
- Symptom: heavy write amplification.
- Recovery: tune file sizes, batching, MOR/COW choice.
- Prevention: design for update workload.

## 12. Common Mistakes

- Mistake: Treating data lake upserts like OLTP row updates.
- Why it is wrong: lakehouse updates often rewrite files or write delete/change files.
- Better approach: batch updates and design for file-level cost.

- Mistake: Upserting without a stable key.
- Why it is wrong: the system cannot know what row to update.
- Better approach: define unique keys and test duplicates.

## 13. Mini Example

```text
Existing table:
id=1, status=pending

Incoming:
id=1, status=shipped
id=2, status=pending

After upsert:
id=1, status=shipped
id=2, status=pending
```

## 14. Interview Questions

1. What is an upsert?
2. Why are upserts hard on a data lake?
3. How does MERGE work conceptually?
4. What keys are needed?
5. How do CDC and upserts connect?

## 15. Interview Speak

"Upserts on a data lake are implemented through table formats that match incoming records by key, then rewrite affected files or write change/delete files before committing a new snapshot. I would use MERGE for current-state tables but design carefully around keys, ordering, file sizes, and compaction."

## 16. Quick Recall

- One-line summary: Upsert keeps lakehouse tables current by key.
- Three keywords: MERGE, key, CDC.
- One trap: Forgetting out-of-order updates.
- One memory trick: Update if exists, insert if new.
