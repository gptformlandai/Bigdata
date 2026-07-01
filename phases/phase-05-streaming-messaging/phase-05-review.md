# Phase 5 Review: Streaming And Messaging

This review checks whether you understand streaming and messaging from beginner intuition to system design readiness.

## Phase Summary

Phase 5 covered:

- event-driven architecture
- queues vs event streams
- Kafka brokers, topics, partitions, offsets, consumer groups
- Kafka replication, ISR, acknowledgments, retention, compaction, ordering, exactly-once
- Kafka Connect, Kafka Streams, Schema Registry, Avro
- DLQs, consumer lag, and streaming backpressure
- Flink, state, checkpointing, watermarks, event time, windows, late events
- Spark Structured Streaming
- real-time analytics architecture

Main idea:

```text
Streaming systems process facts continuously, so they must handle duplicates, lag, late events, ordering, schemas, state, and recovery.
```

## Checkpoint 1: Topics 107-114

### Quiz

1. What is an event?
2. Queue vs event stream?
3. What is a Kafka topic?
4. What is a partition?
5. What is a consumer group?

### Practical Exercise

Design topics for an e-commerce system:

- orders
- payments
- inventory
- clicks

For each, choose:

- event name
- message key
- partition count assumption
- consumer groups

### Mini System Design Question

> Multiple services need to react to `OrderCreated`. How would you design it?

Strong direction:

- publish `OrderCreated` to Kafka
- key by `order_id`
- separate consumer groups for payment, inventory, analytics, notifications
- schema registry
- idempotent consumers

## Checkpoint 2: Topics 115-121

### Quiz

1. What is Kafka replication factor?
2. What is ISR?
3. `acks=1` vs `acks=all`?
4. Retention vs compaction?
5. What ordering does Kafka guarantee?

### Practical Exercise

For a payment topic, choose:

- replication factor
- `min.insync.replicas`
- producer `acks`
- message key
- retention
- schema strategy

### Mini System Design Question

> How do you make Kafka payment events durable?

Strong direction:

- replication factor 3
- `acks=all`
- `min.insync.replicas=2`
- idempotent producer
- schema registry
- lag and under-replication monitoring

## Checkpoint 3: Topics 122-128

### Quiz

1. Kafka Connect source vs sink?
2. What does Schema Registry protect?
3. Why use Avro?
4. What is a DLQ?
5. What does consumer lag mean?

### Practical Exercise

Design a Kafka-to-data-lake ingestion pipeline:

- source topic
- schema format
- sink connector
- DLQ
- lag monitoring
- retention plan

### Mini System Design Question

> A consumer crashes on one bad event and stops processing. What do you change?

Strong direction:

- classify transient vs permanent errors
- bounded retries
- DLQ bad records
- include error metadata
- alert on DLQ growth
- make processing idempotent

## Checkpoint 4: Topics 129-137

### Quiz

1. Why use Flink?
2. What is state?
3. What does checkpointing save?
4. What is a watermark?
5. Event time vs processing time?
6. Tumbling vs sliding window?
7. What are late events?

### Practical Exercise

Design a real-time revenue dashboard:

- Kafka input topic
- event schema
- stream processor
- window type
- watermark/late policy
- serving store
- raw data lake sink
- monitoring

### Mini System Design Question

> You need ad click metrics within 1 minute, but mobile events can arrive 5 minutes late. How do you design it?

Strong direction:

- event-time windows
- watermarks
- allowed lateness
- preliminary and corrected metrics
- Kafka retention for replay
- DLQ for bad events
- serving store for dashboard

## Must-Know Concepts

You should be able to explain:

- event vs command
- producer, broker, topic, partition, offset
- consumer group and rebalance
- Kafka retention vs compaction
- Kafka ordering per partition
- ISR and producer acks
- consumer lag and backpressure
- Schema Registry and Avro
- DLQ and poison messages
- Flink state and checkpointing
- event time vs processing time
- watermarks and late events
- tumbling/sliding/session windows
- Spark Structured Streaming checkpointing
- real-time analytics architecture

## Common Interview Questions

1. Explain Kafka architecture.
2. Why does Kafka use partitions?
3. How does a consumer group scale?
4. What happens if a Kafka broker fails?
5. What does `acks=all` mean?
6. What is ISR?
7. How do you handle duplicate messages?
8. What is consumer lag and how do you reduce it?
9. What is a DLQ?
10. What is event time?
11. What is a watermark?
12. Flink vs Spark Structured Streaming?

## Hands-On Project

Build a mini streaming mental-model pipeline locally.

### Input Events

```text
event_id, user_id, event_time, arrival_time, amount
```

### Steps

1. Assign events to Kafka partitions by `user_id`.
2. Assign partitions to consumers in a group.
3. Track offsets.
4. Simulate one duplicate event.
5. Deduplicate by `event_id`.
6. Aggregate revenue in 5-minute event-time windows.
7. Use watermark logic to classify late events.
8. Send bad records to a DLQ list.
9. Print lag and window totals.

## Production Checklist

Before designing a streaming system, ask:

- What events are produced?
- What is the schema?
- What is the message key?
- How many partitions?
- What ordering is required?
- What retention is required?
- What replication and acks?
- What consumer groups?
- What is the expected throughput?
- What is acceptable lag?
- Are consumers idempotent?
- What is the DLQ strategy?
- How are schemas evolved?
- Is event time required?
- What watermark and lateness policy?
- What state is stored?
- How are checkpoints configured?
- What is the serving store?
- How do we replay/backfill?
- What is monitored?

## Final Phase 5 Interview Answer

"For streaming, I would model business facts as events, publish them to Kafka topics with clear schemas and keys, choose partitions based on throughput and ordering, and use consumer groups for independent processing. I would configure replication, ISR, and producer acknowledgments based on durability needs. For stream processing, I would use Flink or Spark Structured Streaming depending on latency, state, and ecosystem needs. I would design for idempotency, DLQs, consumer lag, backpressure, event time, watermarks, late events, checkpointing, replay, and monitoring."
