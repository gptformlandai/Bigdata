# Topic 241: Debezium

## 1. Goal

Understand Debezium as a common open-source CDC platform.

## 2. Baby Intuition

Debezium is like a translator between database change logs and event streams.

It reads database changes and publishes them as structured events.

## 3. What It Is

- Simple definition: Debezium captures database changes and emits events.
- Technical definition: Debezium is an open-source CDC platform that reads database transaction logs such as MySQL binlog or PostgreSQL WAL and publishes change events, commonly through Kafka Connect.
- Category: CDC tooling.
- Related terms: Kafka Connect, connector, binlog, WAL, snapshot, offset, schema change, tombstone.

## 4. Why It Exists

Many systems need database changes in real time:

- update lakehouse tables
- sync search indexes
- update caches
- feed downstream services
- capture audit/change history

Debezium provides a standardized way to capture changes from popular databases.

## 5. Where It Fits In A Data Platform

```text
MySQL/Postgres/MongoDB/etc.
  -> Debezium connector
  -> Kafka topics
  -> consumers: lakehouse/search/cache/warehouse
```

## 6. How It Works Step By Step

1. Configure connector for source database.
2. Debezium may take initial snapshot.
3. It reads database change log.
4. It emits change events to Kafka topics.
5. It records offsets/log positions.
6. Consumers process events.
7. Schema changes and deletes are emitted according to configuration.

## 7. How To Use It Practically

Important concepts:

| Concept | Meaning |
|---|---|
| connector | source-specific CDC reader |
| snapshot | initial full table capture |
| offset | connector progress |
| topic | Kafka destination per table/pattern |
| tombstone | delete marker/compaction helper |
| schema history | tracks DDL changes |

Good practices:

- monitor connector lag
- protect database from excessive load
- plan snapshot windows
- handle schema changes
- test delete/tombstone handling
- secure database credentials

## 8. Real-World Scenario

- Product/system: PostgreSQL to Kafka to Iceberg.
- Problem: Order table updates must reach lakehouse within minutes.
- How Debezium helps: reads WAL changes and emits order events to Kafka; Spark/Flink MERGEs into Iceberg.
- What would go wrong without it: scheduled extracts are slower and may miss update/delete details.

## 9. System Design Angle

Use Debezium when:

- open-source CDC is desired
- Kafka is the event backbone
- source databases are supported
- downstream systems need change streams

Be careful with:

- connector reliability
- database permissions
- snapshot consistency
- schema evolution
- ordering by key
- Kafka topic retention/compaction

## 10. Trade-offs

| Pros | Cons |
|---|---|
| popular open-source CDC | operational setup needed |
| integrates with Kafka Connect | source DB log config required |
| captures inserts/updates/deletes | schema changes need handling |
| replayable event topics | connector lag and failures matter |

## 11. Failure Modes

- Failure: Replication slot/log retention misconfigured.
- Symptom: connector falls behind or database log grows.
- Recovery: fix connector and DB config.
- Prevention: lag monitoring.

- Failure: Snapshot overloads source DB.
- Symptom: OLTP performance impact.
- Recovery: throttle or schedule snapshot.
- Prevention: snapshot planning.

- Failure: Consumer ignores tombstones.
- Symptom: deleted rows remain downstream.
- Recovery: replay or repair.
- Prevention: delete tests.

## 12. Common Mistakes

- Mistake: Deploying Debezium without source DB team alignment.
- Why it is wrong: log retention, permissions, and load affect OLTP.
- Better approach: coordinate with database owners.

- Mistake: Assuming CDC event schema never changes.
- Why it is wrong: source DDL changes happen.
- Better approach: schema evolution strategy.

## 13. Mini Example

```text
Postgres table customers
  -> Debezium connector
  -> Kafka topic db.public.customers
  -> Flink upsert to lakehouse customers table
```

## 14. Interview Questions

1. What is Debezium?
2. How does it capture database changes?
3. What is Kafka Connect?
4. What is an initial snapshot?
5. What operational risks exist?

## 15. Interview Speak

"Debezium is an open-source CDC platform, often used with Kafka Connect, that reads database transaction logs and emits change events. I would use it for near-real-time database replication, while monitoring connector lag, snapshot impact, schema changes, deletes, and database log retention."

## 16. Quick Recall

- One-line summary: Debezium turns database log changes into event streams.
- Three keywords: connector, snapshot, offset.
- One trap: Snapshot/log impact on source database.
- One memory trick: Database log translator.
