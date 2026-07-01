# Topic 240: CDC

## 1. Goal

Understand change data capture as a way to move database changes into data platforms.

## 2. Baby Intuition

CDC is like watching a database's change diary.

Instead of copying the whole database every time, CDC reads what changed.

## 3. What It Is

- Simple definition: CDC captures inserts, updates, and deletes from a database.
- Technical definition: Change Data Capture extracts row-level database changes from logs, triggers, timestamps, or queries and sends them to downstream systems like Kafka, lakehouses, warehouses, or search indexes.
- Category: Data ingestion pattern.
- Related terms: binlog, WAL, oplog, Debezium, snapshot, replication slot, upsert, delete/tombstone.

## 4. Why It Exists

Batch full extracts are expensive:

```text
copy entire orders table every hour
```

CDC is more efficient:

```text
send only rows that changed
```

CDC supports near-real-time analytics, lakehouse upserts, search indexing, and cache updates.

## 5. Where It Fits In A Data Platform

```text
OLTP database
  -> CDC connector
  -> Kafka/Kinesis/Pub/Sub
  -> lakehouse/warehouse/search/feature store
```

## 6. How It Works Step By Step

1. CDC connector takes an initial snapshot if needed.
2. Connector reads database change log.
3. Each insert/update/delete becomes an event.
4. Events are published to a stream or sink.
5. Downstream consumers apply changes.
6. Offsets/checkpoints track progress.
7. Monitoring tracks lag and failures.

## 7. How To Use It Practically

CDC event contains:

| Field | Meaning |
|---|---|
| operation | insert/update/delete |
| before | old row values |
| after | new row values |
| source | database/table/log position |
| timestamp | when change happened |
| key | primary key |

Good practices:

- use stable primary keys
- handle deletes
- preserve ordering by key
- make sinks idempotent
- monitor lag
- handle schema changes

## 8. Real-World Scenario

- Product/system: MySQL to lakehouse customer table.
- Problem: Customer records change all day and analytics needs current state.
- How CDC helps: database changes stream to Kafka and MERGE into lakehouse table.
- What would go wrong without it: hourly full extracts are slow and stale.

## 9. System Design Angle

Use CDC when:

- OLTP changes must feed analytics/search/ML
- near-real-time replication is needed
- full extracts are too expensive
- deletes/updates matter

Be careful with:

- schema evolution
- ordering
- initial snapshot consistency
- connector lag
- delete/tombstone handling

## 10. Trade-offs

| Pros | Cons |
|---|---|
| low-latency changes | operational complexity |
| avoids full scans | log permissions/setup required |
| captures deletes/updates | schema changes can break consumers |
| supports replay streams | downstream idempotency needed |

## 11. Failure Modes

- Failure: CDC lag grows.
- Symptom: downstream table stale.
- Recovery: scale/tune connector and consumers.
- Prevention: lag alerts.

- Failure: Delete events ignored.
- Symptom: deleted rows remain downstream.
- Recovery: replay with delete handling.
- Prevention: tombstone/delete tests.

- Failure: Schema change breaks consumer.
- Symptom: pipeline fails.
- Recovery: update schema handling.
- Prevention: schema registry/contracts.

## 12. Common Mistakes

- Mistake: Treating CDC as simple append-only events.
- Why it is wrong: updates and deletes need special handling.
- Better approach: model current state and history intentionally.

- Mistake: No initial snapshot plan.
- Why it is wrong: downstream needs starting table state.
- Better approach: snapshot first, then stream changes.

## 13. Mini Example

```text
Database update:
orders.id=10 status changes pending -> shipped

CDC event:
op=update
key=10
before.status=pending
after.status=shipped
```

## 14. Interview Questions

1. What is CDC?
2. Why use CDC instead of full batch extract?
3. What is an initial snapshot?
4. How do you handle deletes?
5. What can go wrong with schema changes?

## 15. Interview Speak

"CDC captures row-level database inserts, updates, and deletes from logs and streams them downstream. I would use it for near-real-time lakehouse, warehouse, search, or feature pipelines, with careful handling of snapshots, ordering, deletes, schema changes, lag, and idempotent sinks."

## 16. Quick Recall

- One-line summary: CDC streams database changes instead of full tables.
- Three keywords: log, change event, upsert.
- One trap: Ignoring deletes.
- One memory trick: Database change diary.
