# Topic 137: Real-Time Analytics Architecture

## 1. Goal

Understand how to design an end-to-end real-time analytics system.

## 2. Baby Intuition

Real-time analytics is like a live scoreboard.

Events happen continuously, and the scoreboard updates quickly instead of waiting until tomorrow.

## 3. What It Is

- Simple definition: Real-time analytics architecture processes events soon after they happen and serves fresh metrics.
- Technical definition: A real-time analytics architecture ingests continuous events, processes them with streaming systems, stores raw and derived data, and serves low-latency dashboards, alerts, or APIs.
- Category: End-to-end streaming system design.
- Related terms: Kafka, Flink, Structured Streaming, materialized view, OLAP store, data lake, dashboard.

## 4. Why It Exists

Batch analytics answers:

```text
What happened yesterday?
```

Real-time analytics answers:

```text
What is happening now?
```

Use cases:

- fraud detection
- live dashboards
- ad metrics
- operational monitoring
- driver location
- inventory alerts
- personalization signals

## 5. Where It Fits In A Data Platform

```text
Applications
  -> Kafka / stream ingestion
  -> Stream processor
  -> Real-time serving store
  -> Dashboard/API/alerts

Also:
  -> Raw data lake for replay/batch
```

## 6. How It Works Step By Step

1. Applications emit events.
2. Events are validated and published to Kafka.
3. Raw events are archived to data lake.
4. Stream processor reads events.
5. Processor handles parsing, dedupe, enrichment, windows, and aggregations.
6. Results are written to serving store.
7. Dashboard/API reads fresh metrics.
8. Monitoring tracks lag, freshness, errors, and throughput.
9. Batch reconciliation corrects long-term truth if needed.

## 7. How To Use It Practically

Common architecture choices:

| Layer | Options |
|---|---|
| ingestion | Kafka, Kinesis, Pub/Sub |
| processing | Flink, Spark Structured Streaming, Kafka Streams |
| raw archive | S3/GCS/ADLS/HDFS |
| serving | Pinot, Druid, ClickHouse, Elasticsearch, Redis, warehouse |
| orchestration | Airflow/Dagster for batch companion jobs |
| monitoring | lag, throughput, error rate, freshness |

## 8. Real-World Scenario

- Product/system: Real-time ad analytics.
- Problem: Advertisers need impressions, clicks, and spend within seconds/minutes.
- How architecture helps: Kafka captures ad events, stream processor aggregates by campaign/window, serving store powers dashboard.
- What would go wrong without it: advertisers see stale metrics and cannot react to campaign performance.

## 9. System Design Angle

Requirements to clarify:

- freshness SLA
- event volume
- event size
- allowed data loss
- duplicate handling
- ordering needs
- late event policy
- query latency
- retention/replay
- security and PII

Common design:

```text
client/server events -> Kafka -> Flink -> Pinot/Druid/ClickHouse -> dashboard
                           -> S3 raw lake for replay
```

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| fresh metrics | higher operational complexity |
| fast alerts | eventual corrections |
| real-time decisions | cost of always-on processing |
| replayable architecture | schema and quality governance |

## 11. Failure Modes

- Failure: producer sends bad schema.
- Symptom: stream processor errors/DLQ grows.
- Recovery: schema rollback and DLQ replay.
- Prevention: Schema Registry and validation.

- Failure: consumer lag grows.
- Symptom: dashboard stale.
- Recovery: scale/tune processor or sink.
- Prevention: lag/freshness alerts.

- Failure: serving store down.
- Symptom: dashboard/API unavailable.
- Recovery: failover/cache/degrade.
- Prevention: HA serving layer.

- Failure: late events.
- Symptom: metrics change after initial display.
- Recovery: corrections/reconciliation.
- Prevention: watermark and lateness policy.

## 12. Common Mistakes

- Mistake: Designing only the happy path.
- Why it is wrong: streaming systems fail through lag, schema, bad records, and sink bottlenecks.
- Better approach: include DLQ, replay, monitoring, and backpressure.

- Mistake: Using Kafka as the dashboard query store.
- Why it is wrong: Kafka is a log, not an OLAP serving database.
- Better approach: write aggregates to a serving store.

## 13. Mini Example

```text
Click event
  -> Kafka topic clickstream
  -> Flink 1-minute campaign aggregation
  -> Pinot realtime table
  -> dashboard query under 1 second
```

## 14. Interview Questions

1. Design a real-time analytics system.
2. Why use Kafka?
3. Where do raw events go?
4. Which stream processor would you choose?
5. How do you handle late events and lag?

## 15. Interview Speak

"For real-time analytics, I would ingest events into Kafka, validate schemas, archive raw events to a data lake for replay, process streams with Flink or Structured Streaming, handle dedupe/windows/late events, and write aggregates to a serving store like Pinot, Druid, ClickHouse, Redis, or Elasticsearch depending on query needs. I would monitor lag, freshness, errors, throughput, and DLQ volume."

## 16. Quick Recall

- One-line summary: Real-time analytics turns live events into fresh metrics.
- Three keywords: Kafka, stream processor, serving store.
- One trap: Querying Kafka directly as the analytics database.
- One memory trick: Live scoreboard needs ingestion, processing, and serving.
