# Topic 200: AWS Kinesis

## 1. Goal

Understand Amazon Kinesis as AWS's managed streaming data service family.

## 2. Baby Intuition

Kinesis is like a managed river of events.

Applications put events into the stream, and consumers process them continuously.

## 3. What It Is

- Simple definition: Kinesis helps ingest and process streaming data on AWS.
- Technical definition: Amazon Kinesis services support collection, buffering, processing, and delivery of streaming records for real-time and near-real-time data applications.
- Category: Managed streaming / event ingestion.
- Related terms: stream, shard, record, producer, consumer, Firehose, Data Streams, Flink, enhanced fan-out.

## 4. Why It Exists

Modern systems produce continuous events:

- clicks
- logs
- IoT readings
- payment events
- app metrics
- security events

Kinesis exists to ingest and deliver these events without building your own streaming cluster.

## 5. Where It Fits In A Data Platform

```text
applications/devices/logs
  -> Kinesis
  -> Lambda/Flink/Firehose/consumers
  -> S3/Redshift/OpenSearch/realtime dashboards
```

## 6. How It Works Step By Step

1. Producer sends records to a stream or delivery service.
2. Records are partitioned, often by partition key.
3. Consumers read records in order within a shard/partition.
4. Stream processors enrich/aggregate/filter events.
5. Outputs are written to S3, warehouse, search, alerts, or APIs.
6. Monitoring tracks lag, throughput, throttling, and failures.

## 7. How To Use It Practically

Common Kinesis patterns:

| Service/Pattern | Use |
|---|---|
| Kinesis Data Streams | custom streaming consumers |
| Kinesis Data Firehose | managed delivery to destinations like S3 |
| Managed streaming with Flink | stateful stream processing |
| Lambda consumer | lightweight event reactions |

Design points:

- choose partition key carefully
- monitor shard/throughput limits
- handle retries and duplicates
- archive raw stream to S3
- use DLQ/error path where possible

## 8. Real-World Scenario

- Product/system: Real-time clickstream ingestion.
- Problem: Millions of user events must land in S3 and power near-real-time metrics.
- How Kinesis helps: producers send events to stream/Firehose; events are delivered to S3 and processed by stream consumers.
- What would go wrong without it: applications must directly write to many consumers and handle buffering/retries.

## 9. System Design Angle

Use Kinesis when:

- AWS-native streaming is needed
- event ingestion is continuous
- consumers need near-real-time data
- managed delivery to S3/analytics systems is useful

Compare:

- Kafka/MSK for Kafka ecosystem and portability
- Kinesis for AWS-managed streaming integration
- SQS for queueing tasks/messages

## 10. Trade-offs

| Pros | Cons |
|---|---|
| managed AWS streaming | AWS-specific |
| integrates with S3/Lambda/Flink | partition/shard design matters |
| good for event ingestion | ordering limited by shard/key |
| scalable stream processing | duplicates/retries must be handled |
| Firehose simplifies delivery | less flexible than custom consumers |

## 11. Failure Modes

- Failure: Hot partition key.
- Symptom: one shard throttles/backs up.
- Recovery: change key/sharding strategy.
- Prevention: choose high-cardinality balanced keys.

- Failure: Consumer lag grows.
- Symptom: real-time outputs stale.
- Recovery: scale consumers or increase capacity.
- Prevention: lag alerts.

- Failure: Bad records poison processing.
- Symptom: consumer repeatedly fails.
- Recovery: DLQ/quarantine bad records.
- Prevention: schema validation.

## 12. Common Mistakes

- Mistake: Assuming total ordering across whole stream.
- Why it is wrong: ordering is usually scoped by shard/partition key.
- Better approach: design ordering by entity key where needed.

- Mistake: Forgetting duplicate handling.
- Why it is wrong: retries can produce duplicates.
- Better approach: idempotent consumers and dedupe keys.

## 13. Mini Example

```text
click event
  -> Kinesis stream partitioned by user_id
  -> Flink/Lambda consumer
  -> S3 raw archive and realtime metrics
```

## 14. Interview Questions

1. What is Kinesis?
2. What is a shard/partition key?
3. Kinesis vs Kafka?
4. How do you handle consumer lag?
5. How do you archive streaming data?

## 15. Interview Speak

"Kinesis is AWS managed streaming for continuous event ingestion and processing. I would choose partition keys carefully, monitor lag and throughput, handle duplicates/idempotency, validate schemas, and often archive raw events to S3 for replay."

## 16. Quick Recall

- One-line summary: Kinesis is AWS managed event streaming.
- Three keywords: stream, partition key, consumer lag.
- One trap: Assuming global ordering.
- One memory trick: Managed river of events.
