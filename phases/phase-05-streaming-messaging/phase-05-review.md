# Phase 5 Review: Streaming And Messaging

This review checks whether you understand event-driven systems, Kafka, Flink, stream-time concepts, and real-time analytics architecture.

## Phase Summary

Phase 5 covered:

- event-driven architecture
- queues vs event streams
- Kafka brokers, topics, partitions, offsets, consumer groups
- Kafka replication, ISR, producer acks, retention, compaction, ordering, exactly-once
- Kafka Connect, Kafka Streams, Schema Registry, Avro, DLQ, lag, backpressure
- Flink, state, checkpointing, watermarks, event time, windows, late events
- Spark Structured Streaming
- real-time analytics architecture

Main idea:

```text
Streaming systems process events continuously, so correctness depends on ordering, offsets, state, time, retries, schemas, lag, and failure handling.
```

## Checkpoint 1: Topics 107-108

Topics:

- Event-driven architecture
- Message queues vs event streams

### Quiz

1. What is an event?
2. Why does event-driven architecture decouple systems?
3. What is the difference between an event and a command?
4. When would you use a queue?
5. When would you use an event stream?

### Practical Exercise

For an e-commerce order flow, list events:

- order created
- payment captured
- inventory reserved
- order shipped

Then decide which consumers need each event.

### Mini System Design Question

> Multiple systems need to react when a payment succeeds. Would you use direct service calls, a queue, or an event stream?

Strong direction:

- Use an event stream when many independent consumers need the same event.
- Consumers can include fraud, email, analytics, ledger, and data lake.
- Mention schema, idempotency, replay, and eventual consistency.

## Checkpoint 2: Topics 109-121

Topics:

- Kafka overview
- broker, topic, partition, offset, consumer group
- replication, ISR, acks, retention, compaction
- ordering, exactly-once semantics

### Quiz

1. What is Kafka?
2. What does a broker do?
3. What is a topic?
4. What is a partition?
5. What is an offset?
6. What is a consumer group?
7. What is ISR?
8. What does `acks=all` mean?
9. What does retention control?
10. What ordering does Kafka guarantee?

### Practical Exercise

Design a Kafka topic for payment events:

- topic name
- partition key
- partition count assumption
- replication factor
- retention
- producer acks
- schema strategy
- consumer groups

### Mini System Design Question

> A payment event must not be acknowledged unless safely replicated. What Kafka settings matter?

Strong direction:

- replication factor 3
- `acks=all`
- `min.insync.replicas=2`
- idempotent producer
- monitor ISR/under-replication
- choose key for ordering

## Checkpoint 3: Topics 122-128

Topics:

- Kafka Connect
- Kafka Streams
- Schema Registry
- Avro with Kafka
- Dead letter queues
- Consumer lag
- Backpressure in streaming

### Quiz

1. Source connector vs sink connector?
2. Kafka Connect vs Kafka Streams?
3. Why use Schema Registry?
4. Why is Avro useful?
5. What goes into a DLQ?
6. How is consumer lag calculated?
7. What causes backpressure?

### Practical Exercise

Design a Kafka-to-S3 ingestion pipeline:

- input topic
- schema format
- connector type
- file format
- error handling
- DLQ
- lag monitoring

### Mini System Design Question

> A consumer fails every time it sees one malformed event and stops processing. What should you do?

Strong direction:

- classify retryable vs non-retryable errors
- bounded retries
- DLQ with original payload and error
- commit offset safely after DLQ write
- monitor DLQ volume

## Checkpoint 4: Topics 129-137

Topics:

- Apache Flink
- Flink state
- Flink checkpointing
- Flink watermarks
- Event time vs processing time
- Windowing
- Late events
- Spark Structured Streaming
- Real-time analytics architecture

### Quiz

1. Kafka vs Flink?
2. What is Flink state?
3. What does checkpointing save?
4. What is a watermark?
5. Event time vs processing time?
6. Tumbling vs sliding vs session window?
7. What is a late event?
8. Structured Streaming vs Flink?

### Practical Exercise

Design a 5-minute active users metric:

- source topic
- event timestamp
- key
- window type
- watermark delay
- late event policy
- output sink
- monitoring

### Mini System Design Question

> Design a real-time ad analytics dashboard showing impressions and clicks by campaign with less than 1 minute freshness.

Strong direction:

- events to Kafka
- schema validation
- Flink or Structured Streaming processor
- event-time windows
- watermark and late policy
- raw archive to data lake
- serving store like Pinot/Druid/ClickHouse
- monitor lag, freshness, DLQ, errors

## Must-Know Concepts

You should be comfortable explaining:

- event-driven architecture
- queue vs stream
- Kafka broker/topic/partition/offset
- consumer groups and rebalancing
- replication, ISR, acks
- retention vs compaction
- ordering per partition
- exactly-once scope
- Kafka Connect vs Kafka Streams
- Schema Registry and Avro
- DLQ and poison messages
- lag and backpressure
- Flink state and checkpointing
- watermarks and event time
- windowing and late events
- Structured Streaming micro-batches
- real-time analytics serving stores

## Common Interview Questions

1. Explain Kafka architecture.
2. How do Kafka partitions provide scale?
3. What is consumer lag and how do you reduce it?
4. How does Kafka guarantee ordering?
5. What is ISR?
6. What are producer acks?
7. What is the difference between retention and compaction?
8. What does exactly-once mean in Kafka?
9. How do you handle poison messages?
10. What is a watermark?
11. How do you handle late events?
12. Flink vs Spark Structured Streaming?
13. Design a real-time dashboard.

## Hands-On Project

Build a local streaming simulator.

### Input

Use events:

```text
event_id,user_id,event_type,event_time,arrival_time
```

### Steps

1. Partition events by `user_id`.
2. Assign partitions to consumers in a consumer group.
3. Track offsets per partition.
4. Simulate at-least-once retry and duplicate event.
5. Deduplicate by `event_id`.
6. Apply 5-minute event-time windows.
7. Use watermark = max event time - 2 minutes.
8. Send very late events to DLQ.
9. Print lag and final window counts.

### What This Teaches

- partition keys
- offsets
- consumer groups
- delivery semantics
- idempotency
- event time
- watermarks
- late events

## Production Checklist

Before shipping a streaming pipeline, ask:

- What events are produced?
- What is the schema?
- Is Schema Registry used?
- What is the topic name?
- What is the partition key?
- What ordering is required?
- What is the partition count?
- What is replication factor?
- What are producer acks?
- What is retention?
- Is compaction needed?
- What consumer groups exist?
- How are offsets committed?
- What delivery semantics are required?
- Are consumers idempotent?
- What is the DLQ policy?
- How is lag monitored?
- What is the backpressure strategy?
- Is event time or processing time used?
- What watermark delay is chosen?
- How are late events handled?
- Where are raw events archived?
- What serving store powers dashboards?

## Final Phase 5 Interview Answer

"For streaming systems, I start with the event model and correctness needs. Kafka is the event backbone: producers write to partitioned topics, consumers read by offsets, consumer groups scale processing, and replication/ISR/acks protect durability. I use Schema Registry and Avro for contracts, DLQs for poison records, and lag/backpressure monitoring for operations. For stateful event-time processing, I consider Flink or Structured Streaming, with checkpoints, watermarks, windows, and late-event policy. For real-time analytics, I archive raw events, process streams into aggregates, and serve them from an OLAP/serving store while monitoring freshness, errors, and lag."
