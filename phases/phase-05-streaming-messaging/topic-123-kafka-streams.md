# Topic 123: Kafka Streams

## 1. Goal

Understand Kafka Streams as a Java library for building stream processing apps on Kafka.

## 2. Baby Intuition

Kafka stores the moving events.

Kafka Streams lets your app process those events as they flow:

```text
read topic -> transform/join/aggregate -> write topic
```

## 3. What It Is

- Simple definition: Kafka Streams is a library for processing Kafka data.
- Technical definition: Kafka Streams is a client library for building distributed stream processing applications that read from Kafka topics, maintain state, and write results back to Kafka.
- Category: Stream processing library.
- Related terms: KStream, KTable, state store, topology, exactly-once, changelog topic.

## 4. Why It Exists

Teams need to process events continuously:

- filter events
- enrich events
- aggregate counts
- join streams
- maintain state
- create derived topics

Kafka Streams exists so applications can do this without running a separate processing cluster like Flink.

## 5. Where It Fits In A Data Platform

```text
Kafka input topics -> Kafka Streams app -> Kafka output topics
```

It runs as an application, usually Java/Scala, deployed like a service.

## 6. How It Works Step By Step

1. Define topology.
2. App subscribes to input topics.
3. App processes records partition by partition.
4. State stores keep local state when needed.
5. Changelog topics back up state.
6. Results are written to output topics.
7. Multiple app instances share partitions.

## 7. How To Use It Practically

Conceptual Java-like flow:

```java
KStream<String, Order> orders = builder.stream("orders");

orders
    .filter((key, order) -> order.status().equals("paid"))
    .to("paid-orders");
```

Use cases:

- topic-to-topic transformations
- small/medium stream apps
- stateful aggregations
- event enrichment

## 8. Real-World Scenario

- Product/system: Fraud signal enrichment.
- Problem: Enrich payment events and write risk features to another topic.
- How Kafka Streams helps: Runs as an app that reads, transforms, and writes Kafka topics.
- What would go wrong without it: custom consumers/producers must handle state and offsets manually.

## 9. System Design Angle

Kafka Streams is good when:

- Kafka is source and sink
- team is JVM-friendly
- app-level deployment is preferred
- processing is close to Kafka

Flink may be better when:

- complex event-time processing
- advanced stateful streaming
- large-scale windows
- strong operational stream processing platform needed

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| no separate cluster | JVM library/app management |
| tight Kafka integration | Kafka-centric source/sink |
| local state stores | state restore complexity |
| exactly-once support | operational tuning |

## 11. Failure Modes

- Failure: app instance crashes.
- Symptom: partitions reassigned to other instances.
- Recovery: state restored from changelog topics.
- Prevention: stable deployment and monitoring.

- Failure: state store grows too large.
- Symptom: disk pressure/slow restore.
- Recovery: tune retention/state design.
- Prevention: size state and monitor.

## 12. Common Mistakes

- Mistake: Thinking Kafka Streams is a Kafka broker feature.
- Why it is wrong: it is a client library running in your app.
- Better approach: deploy and monitor it like an application.

- Mistake: Ignoring state restore time.
- Why it is wrong: large state can delay recovery.
- Better approach: monitor state and changelog topics.

## 13. Mini Example

```text
orders -> filter paid -> paid-orders
orders -> group by customer -> customer-order-counts
```

## 14. Interview Questions

1. What is Kafka Streams?
2. Kafka Streams vs Kafka Connect?
3. What is a state store?
4. What is a changelog topic?
5. Kafka Streams vs Flink?

## 15. Interview Speak

"Kafka Streams is a Java client library for stream processing on Kafka. It lets applications read Kafka topics, transform, join, aggregate, maintain local state stores, and write results back to Kafka. It is Kafka-centric and easy to deploy as an app, while Flink is stronger for advanced event-time/stateful processing."

## 16. Quick Recall

- One-line summary: Kafka Streams is app-level Kafka stream processing.
- Three keywords: KStream, state store, topology.
- One trap: Confusing it with Kafka Connect.
- One memory trick: Kafka Streams is code that processes Kafka's timeline.
