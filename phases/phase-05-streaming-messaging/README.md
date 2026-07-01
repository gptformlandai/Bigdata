# Phase 5: Streaming And Messaging

Phase 5 teaches streaming and messaging from baby steps to production/interview depth.

The mental model is:

```text
events happen continuously -> producers publish them -> messaging/streaming systems store and deliver them -> consumers process them -> real-time outputs are updated
```

This phase is very important for Big Data because modern systems do not only process yesterday's files. They also process clicks, payments, logs, fraud signals, locations, metrics, and database changes as they happen.

## Topics

| # | Topic | Status |
|---:|---|---|
| 107 | Event-driven architecture | Complete |
| 108 | Message queues vs event streams | Complete |
| 109 | Apache Kafka overview | Complete |
| 110 | Kafka broker | Complete |
| 111 | Kafka topic | Complete |
| 112 | Kafka partition | Complete |
| 113 | Kafka offset | Complete |
| 114 | Kafka consumer group | Complete |
| 115 | Kafka replication | Complete |
| 116 | Kafka ISR | Complete |
| 117 | Kafka producer acknowledgments | Complete |
| 118 | Kafka retention | Complete |
| 119 | Kafka compaction | Complete |
| 120 | Kafka ordering guarantees | Complete |
| 121 | Kafka exactly-once semantics | Complete |
| 122 | Kafka Connect | Complete |
| 123 | Kafka Streams | Complete |
| 124 | Schema Registry | Complete |
| 125 | Avro with Kafka | Complete |
| 126 | Dead letter queues | Complete |
| 127 | Consumer lag | Complete |
| 128 | Backpressure in streaming | Complete |
| 129 | Apache Flink | Complete |
| 130 | Flink state | Complete |
| 131 | Flink checkpointing | Complete |
| 132 | Flink watermarks | Complete |
| 133 | Event time vs processing time | Complete |
| 134 | Windowing | Complete |
| 135 | Late events | Complete |
| 136 | Spark Structured Streaming | Complete |
| 137 | Real-time analytics architecture | Complete |

## Phase Goal

By the end of this phase, you should be able to explain:

- why event-driven systems exist
- how queues differ from event streams
- how Kafka uses brokers, topics, partitions, offsets, consumer groups, replication, ISR, acks, retention, and compaction
- how schema governance works with Schema Registry and Avro
- how to handle poison messages, lag, and backpressure
- why Flink exists and how state, checkpoints, watermarks, windows, and late events work
- how Spark Structured Streaming fits
- how to design a real-time analytics architecture

## Suggested Study Flow

1. Read Topics 107-108 for the basic mental model.
2. Read Topics 109-121 for Kafka fundamentals.
3. Read Topics 122-128 for Kafka ecosystem and operational patterns.
4. Read Topics 129-135 for Flink and event-time stream processing.
5. Read Topics 136-137 for Structured Streaming and real-time architecture.
6. Finish with `phase-05-review.md`.
