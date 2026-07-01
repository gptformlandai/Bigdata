# Topic 268: Design CDC Pipeline From MySQL To Lakehouse

## 1. Goal

Design a reliable change data capture pipeline that moves MySQL inserts, updates, and deletes into a lakehouse table.

## 2. Baby Intuition

MySQL keeps a diary of row changes in its binlog.

CDC reads that diary and applies the same changes to the lakehouse.

## 3. Requirements

Clarify:

- Which MySQL tables are in scope?
- Is the lakehouse table current-state, history, or both?
- What freshness is required?
- How are deletes handled?
- What schema changes are expected?
- Do we need initial snapshot?

## 4. Functional Requirements

- take consistent initial snapshot
- read ongoing MySQL binlog changes
- publish changes to stream
- apply inserts, updates, and deletes to lakehouse
- preserve ordering per primary key
- handle schema evolution
- monitor lag and failures
- support replay and backfill

## 5. Non-Functional Requirements

- low source database impact
- near-real-time freshness
- idempotent sink writes
- fault tolerance
- exactly-once effect where possible
- schema compatibility
- secure data movement

## 6. Capacity Estimation

Example:

```text
orders table: 2B rows
daily changes: 100M
peak changes: 20K/sec
average CDC event: 1 KB
= about 100 GB/day raw change events
```

Also estimate snapshot size separately from daily change volume.

## 7. Events And APIs

CDC event:

```json
{
  "table": "orders",
  "op": "update",
  "key": {"order_id": 123},
  "before": {"status": "pending"},
  "after": {"order_id": 123, "status": "shipped", "amount": 50},
  "binlog_file": "mysql-bin.001",
  "binlog_pos": 98765,
  "event_time": "2026-07-02T10:00:00Z"
}
```

## 8. Data Model

Raw CDC table:

```text
bronze_mysql_orders_cdc(ingest_time, source_table, op, key, before, after, binlog_file, binlog_pos)
```

Current-state lakehouse table:

```text
silver_orders(order_id, customer_id, status, amount, updated_at, is_deleted)
```

History table:

```text
orders_change_history(order_id, op, before, after, source_lsn, event_time)
```

## 9. High-Level Architecture

```text
MySQL
  -> Debezium/MySQL CDC connector
  -> Kafka topic per table
  -> schema registry
  -> stream/batch merge job
  -> lakehouse table
  -> warehouse/BI/ML consumers
```

## 10. Data Flow

1. CDC connector takes initial snapshot.
2. Connector reads MySQL binlog from a known position.
3. Change events are published to Kafka.
4. Raw CDC events are stored in bronze.
5. Merge job groups changes by table/key.
6. Inserts and updates upsert into lakehouse table.
7. Deletes mark row deleted or remove row depending on policy.
8. Checkpoints store processed offsets.

## 11. Deep Dive Components

Initial snapshot:

- captures starting state
- must align with binlog position
- can be large and long-running

Ordering:

- preserve order for same primary key
- partition Kafka by primary key
- avoid applying old update after new update

Deletes:

- hard delete from current table
- soft delete with `is_deleted`
- tombstone event for downstream consumers

## 12. Scaling And Partitioning

- Kafka partition by table plus primary key hash.
- Lakehouse partition by business date when useful, not by high-cardinality key.
- Use merge batching to avoid tiny commits.
- Compact small files after frequent upserts.
- Split very large tables into separate topics/jobs.

## 13. Consistency And Correctness

- Idempotent merge by primary key and source offset.
- Store source binlog position/LSN in target.
- Reject out-of-order older events.
- Schema evolution must be compatible or quarantined.
- Reconcile row counts/checksums periodically.

## 14. Failure Handling

| Failure | Handling |
|---|---|
| connector stops | resume from stored offset |
| Kafka lag grows | scale connector/consumers |
| schema change breaks sink | DLQ and schema workflow |
| duplicate event | idempotent merge |
| missed delete | replay raw CDC and validate tombstones |
| bad merge job | time travel rollback and replay |

## 15. Monitoring, Cost, And Security

Monitor:

- connector lag
- Kafka lag
- lakehouse merge latency
- schema errors
- delete counts
- source vs target reconciliation

Cost:

- batch merge commits
- compact files
- expire old snapshots
- retain raw CDC only as long as needed for replay/audit

Security:

- use least-privilege MySQL replication user
- encrypt transport
- mask/tokenize sensitive columns
- restrict raw CDC access
- audit access and schema changes

## 16. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| CDC instead of full extract | fresh and efficient | operational complexity |
| soft deletes | audit-friendly | queries must filter deleted rows |
| frequent merges | fresher target | more table commits/files |
| batch merges | cheaper | higher latency |

## 17. Interview-Ready Final Answer

"I would use Debezium or a MySQL CDC connector to take an initial snapshot and then read binlog changes into Kafka, partitioned by primary key to preserve per-key ordering. Raw CDC events land in bronze for replay. A merge job applies inserts, updates, and deletes into lakehouse tables using idempotent upserts and source offsets. I would handle schema evolution through a registry and DLQ, monitor connector and merge lag, reconcile source and target counts, compact small files, and use time travel rollback plus replay for recovery."

## 18. Quick Recall

- One-line summary: MySQL CDC copies row changes from binlog to lakehouse with idempotent merges.
- Core tools: MySQL binlog, Debezium, Kafka, schema registry, lakehouse MERGE.
- Main trap: ignoring deletes and schema changes.
- Memory trick: database diary applied to the lake.

