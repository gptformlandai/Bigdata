# Topic 137: Real-Time Analytics Architecture

## 1. Goal

Understand how to design an end-to-end real-time analytics system using streaming and messaging tools.

## 2. Baby Intuition

Batch analytics is like checking yesterday's sales report in the morning.

Real-time analytics is like watching the scoreboard update while the game is happening.

The system must continuously collect events, process them, and update results quickly.

## 3. What It Is

- Simple definition: Real-time analytics architecture processes events quickly after they happen.
- Technical definition: It is an architecture that ingests streaming events, processes them with low latency, stores/serves derived results, and monitors correctness, freshness, and failures.
- Category: Streaming system design.
- Related terms: Kafka, Flink, Spark Structured Streaming, OLAP store, dashboard, feature store.

## 4. Why It Exists

Some decisions cannot wait for tomorrow's batch job.

Examples:

- fraud detection
- live dashboards
- ad campaign performance
- operational alerts
- driver/rider matching
- inventory alerts
- real-time personalization

## 5. Where It Fits In A Data Platform

```text
Apps/DB/Logs
  -> Kafka/Kinesis/PubSub
  -> Flink/Spark/Kafka Streams
  -> Serving store + Data lake
  -> Dashboard/API/ML
```

Common serving stores:

- Druid
- Pinot
- ClickHouse
- Elasticsearch/OpenSearch
- Redis
- Cassandra/DynamoDB
- warehouse/lakehouse for near-real-time

## 6. How It Works Step By Step

1. Applications emit events.
2. Events are validated and serialized.
3. Events are written to Kafka topics.
4. Stream processor consumes events.
5. Processor handles duplicates, state, windows, late events.
6. Results are written to serving store.
7. Raw events are also stored in lake for replay/backfill.
8. Dashboards query serving store.
9. Monitoring watches lag, freshness, error rate, DLQ, checkpoint health.

## 7. How To Use It Practically

Design checklist:

- event schema
- Kafka topic and partition key
- retention period
- consumer group
- processing engine
- windowing/event-time logic
- state and checkpointing
- output store
- DLQ
- replay/backfill plan
- monitoring and alerts

## 8. Real-World Scenario

- Product/system: Real-time ad analytics.
- Problem: Advertisers want impressions, clicks, spend, and CTR within seconds/minutes.
- How architecture helps: Kafka ingests events; Flink aggregates windows; Pinot/Druid serves dashboard; lake stores raw events for backfill.
- What would go wrong without it: batch reports would be stale and advertisers could not react quickly.

## 9. System Design Angle

Requirements to clarify:

- latency target: seconds, minutes, sub-second?
- throughput: events/sec and event size
- accuracy: exact vs approximate
- ordering: per user/campaign/order?
- late data tolerance
- retention/replay needs
- dashboard query patterns
- failure recovery
- cost limits

Architecture choices:

- Kafka for durable event stream
- Flink for low-latency stateful event-time processing
- Spark Structured Streaming for near-real-time lakehouse ETL
- Pinot/Druid/ClickHouse for real-time OLAP
- S3/data lake for raw replay

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| fresh insights | operational complexity |
| fast detection/reaction | harder correctness |
| replayable event log | storage and retention cost |
| stateful metrics | checkpoint/state management |
| live dashboards | serving store tuning |

## 11. Failure Modes

- Failure: Kafka consumer lag grows.
- Symptom: dashboard stale.
- Recovery: scale/optimize consumers.
- Prevention: lag alerts.

- Failure: bad event schema.
- Symptom: processor fails or DLQ grows.
- Recovery: rollback/fix/replay.
- Prevention: schema registry.

- Failure: stream processor checkpoint fails.
- Symptom: recovery risk.
- Recovery: fix state/checkpoint storage.
- Prevention: checkpoint monitoring.

- Failure: serving store slow.
- Symptom: dashboard query latency high.
- Recovery: tune indexes/segments/resources.
- Prevention: capacity planning.

## 12. Common Mistakes

- Mistake: Designing only happy path.
- Why it is wrong: streaming systems fail through lag, duplicates, late events, and bad schemas.
- Better approach: design replay, DLQ, idempotency, checkpointing, and monitoring.

- Mistake: Calling it real-time without latency SLA.
- Why it is wrong: real-time can mean milliseconds or minutes.
- Better approach: state exact freshness/latency target.

## 13. Interview Speak

"For real-time analytics, I would ingest events into Kafka with clear schemas and partition keys, process them using Flink or Spark Structured Streaming depending on latency/state needs, write raw events to a lake for replay, and serve aggregates from a low-latency OLAP store like Pinot, Druid, or ClickHouse. I would design for lag, duplicates, late events, DLQs, checkpointing, schema evolution, and monitoring."

## 14. Quick Recall

- One-line summary: Real-time analytics turns event streams into fresh queryable metrics.
- Three keywords: Kafka, stream processor, serving store.
- One trap: No replay or late-event plan.
- One memory trick: Live scoreboard for events.
