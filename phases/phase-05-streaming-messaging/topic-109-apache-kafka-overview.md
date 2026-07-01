# Topic 109: Apache Kafka Overview

## 1. Goal

Understand Kafka as a distributed event streaming platform used to store and move real-time events.

## 2. Baby Intuition

Kafka is like a durable event notebook.

Producers keep appending new events. Consumers read events at their own pace. Kafka remembers the events for a configured time, so consumers can catch up or replay.

## 3. What It Is

- Simple definition: Kafka stores streams of events and lets many consumers read them.
- Technical definition: Apache Kafka is a distributed event streaming platform that stores records in partitioned, replicated topics and lets producers publish and consumers subscribe by offset.
- Category: Distributed event streaming platform.
- Related terms: broker, topic, partition, offset, producer, consumer, consumer group, retention.

## 4. Why It Exists

Kafka exists because modern systems need to:

- handle high-volume events
- decouple producers from consumers
- replay events
- support many independent consumers
- process logs, clicks, metrics, and CDC in real time
- buffer spikes between fast producers and slower consumers

Without Kafka, teams often build many direct service calls or fragile custom log pipelines.

## 5. Where It Fits In A Data Platform

```text
Applications / Databases / Devices
  -> Kafka
  -> Stream processors / data lake / dashboards / ML / search
```

Kafka is usually the ingestion and event backbone.

## 6. How It Works Step By Step

1. Producer creates event.
2. Producer sends event to Kafka topic.
3. Kafka appends event to a partition.
4. Event gets an offset.
5. Kafka replicates partition data.
6. Consumers read events by offset.
7. Consumers commit progress.
8. Events remain until retention/compaction rules remove them.

## 7. How To Use It Practically

Common commands:

```bash
kafka-topics --bootstrap-server localhost:9092 --create --topic orders --partitions 3 --replication-factor 3
kafka-console-producer --bootstrap-server localhost:9092 --topic orders
kafka-console-consumer --bootstrap-server localhost:9092 --topic orders --from-beginning
```

Basic event:

```json
{"event_id":"e1","event_type":"OrderCreated","order_id":"o1"}
```

## 8. Real-World Scenario

- Product/system: Real-time fraud detection.
- Problem: Payment events must be processed immediately by fraud logic while also saved for analytics.
- How Kafka helps: Payment service publishes events once; fraud, analytics, and lake consumers read independently.
- What would go wrong without it: Direct calls and duplicate pipelines would be brittle.

## 9. System Design Angle

Choose Kafka when:

- high-throughput event ingestion is needed
- multiple consumers need same events
- replay is useful
- consumers may be slower than producers
- ordering per key matters

Avoid Kafka when:

- only a tiny simple task queue is needed
- team cannot operate it
- strict synchronous request/response is required

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| high-throughput event backbone | operational complexity |
| replayable events | offset management |
| multiple independent consumers | schema governance needed |
| decoupling | eventual consistency |

## 11. Failure Modes

- Failure: Broker down.
- Symptom: some partitions unavailable if no healthy replica/leader.
- Recovery: leader election and replication.
- Prevention: replication factor, monitoring.

- Failure: Consumer behind.
- Symptom: lag grows.
- Recovery: scale/tune consumers.
- Prevention: monitor lag.

- Failure: Bad event schema.
- Symptom: consumers fail.
- Recovery: DLQ/schema rollback.
- Prevention: Schema Registry and compatibility checks.

## 12. Common Mistakes

- Mistake: Thinking Kafka is just a queue.
- Why it is wrong: Kafka is a retained event log with replay and consumer groups.
- Better approach: describe topics, partitions, offsets, and retention.

- Mistake: Assuming Kafka gives global order.
- Why it is wrong: order is within a partition.
- Better approach: key events correctly.

## 13. Mini Example

```text
orders topic
  partition 0: offset 0, 1, 2
  partition 1: offset 0, 1, 2
  partition 2: offset 0, 1, 2
```

## 14. Interview Questions

1. What is Kafka?
2. Why use Kafka instead of direct service calls?
3. What are topic, partition, and offset?
4. How does Kafka support replay?
5. What are Kafka's trade-offs?

## 15. Interview Speak

"Kafka is a distributed event streaming platform. Producers append records to partitioned topics, Kafka stores them durably with replication and retention, and consumers read by offset. It is useful for high-throughput event ingestion, decoupling systems, replay, and multiple independent consumers."

## 16. Quick Recall

- One-line summary: Kafka is a distributed replayable event log.
- Three keywords: topic, partition, offset.
- One trap: Calling Kafka only a queue.
- One memory trick: Kafka is a durable event notebook.
