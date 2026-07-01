# Topic 122: Kafka Connect

## 1. Goal

Understand Kafka Connect as a framework for moving data into and out of Kafka without writing custom producer/consumer code.

## 2. Baby Intuition

Kafka Connect is like plug-and-play plumbing.

Instead of writing custom code to move data from MySQL to Kafka or Kafka to S3, you configure a connector.

## 3. What It Is

- Simple definition: Kafka Connect moves data between Kafka and external systems.
- Technical definition: Kafka Connect is a distributed integration framework for running source and sink connectors that import data into Kafka or export data from Kafka.
- Category: Kafka integration framework.
- Related terms: source connector, sink connector, worker, task, connector config, offset storage.

## 4. Why It Exists

Many systems need to connect to Kafka:

- databases
- files
- S3/data lakes
- Elasticsearch
- warehouses
- CDC tools

Writing custom integration code for every source/sink is repetitive and risky.

Kafka Connect provides reusable connectors and distributed runtime.

## 5. Where It Fits In A Data Platform

```text
External source -> Source Connector -> Kafka -> Sink Connector -> External sink
```

Examples:

- MySQL CDC to Kafka
- Kafka to S3
- Kafka to Elasticsearch
- Kafka to JDBC sink

## 6. How It Works Step By Step

Source connector:

1. Reads from external source.
2. Converts records to Kafka format.
3. Writes records to Kafka topics.
4. Tracks source offsets.

Sink connector:

1. Reads Kafka topic records.
2. Converts records for target system.
3. Writes to external sink.
4. Commits Kafka offsets.

Connect cluster:

- workers run connectors
- connectors split work into tasks
- configs define behavior

## 7. How To Use It Practically

Example connector config shape:

```json
{
  "name": "orders-jdbc-source",
  "config": {
    "connector.class": "JdbcSourceConnector",
    "connection.url": "jdbc:mysql://db:3306/shop",
    "table.whitelist": "orders",
    "topic.prefix": "mysql.",
    "mode": "timestamp",
    "timestamp.column.name": "updated_at"
  }
}
```

Common API:

```bash
curl -X POST http://connect:8083/connectors -H "Content-Type: application/json" --data @connector.json
```

## 8. Real-World Scenario

- Product/system: Data lake ingestion.
- Problem: Need to move Kafka clickstream events into S3.
- How Kafka Connect helps: S3 sink connector writes topic records to files.
- What would go wrong without it: custom consumers must handle batching, retries, schema, and failures.

## 9. System Design Angle

Use Kafka Connect when:

- integration is common/reusable
- connector exists and is mature
- team wants less custom code
- source/sink offsets matter

Be careful with:

- connector scaling
- schema evolution
- sink idempotency
- poison records
- source database load

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| less custom code | connector configuration complexity |
| distributed integration runtime | connector limitations |
| offset tracking | operational monitoring |
| reusable ecosystem | plugin/version management |

## 11. Failure Modes

- Failure: connector task fails on bad record.
- Symptom: connector stops or retries.
- Recovery: DLQ/config fix.
- Prevention: schema validation and error tolerance config.

- Failure: sink unavailable.
- Symptom: connector lag grows.
- Recovery: restore sink and catch up.
- Prevention: monitor task status and lag.

## 12. Common Mistakes

- Mistake: Assuming connector handles every edge case.
- Why it is wrong: sink semantics and schema issues still matter.
- Better approach: test failure/retry/idempotency.

- Mistake: No monitoring.
- Why it is wrong: connectors can silently fall behind.
- Better approach: monitor task status, lag, errors.

## 13. Mini Example

```text
Debezium MySQL source -> Kafka topics -> S3 sink connector -> data lake
```

## 14. Interview Questions

1. What is Kafka Connect?
2. Source connector vs sink connector?
3. What are workers and tasks?
4. How does Connect track progress?
5. What can go wrong with connectors?

## 15. Interview Speak

"Kafka Connect is Kafka's integration framework for moving data between Kafka and external systems using source and sink connectors. It reduces custom ingestion code, runs distributed connector tasks, and tracks offsets, but still requires monitoring, schema handling, and failure strategy."

## 16. Quick Recall

- One-line summary: Kafka Connect is plug-and-play data movement for Kafka.
- Three keywords: source, sink, connector.
- One trap: Treating connectors as zero-ops.
- One memory trick: Connect is Kafka plumbing.
