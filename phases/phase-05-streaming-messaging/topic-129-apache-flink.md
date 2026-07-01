# Topic 129: Apache Flink

## 1. Goal

Understand Apache Flink as a distributed stream processing engine for stateful, low-latency, event-time processing.

## 2. Baby Intuition

Kafka stores the moving event stream.

Flink is the worker system that continuously processes that stream:

```text
read events -> remember state -> compute results -> write outputs
```

## 3. What It Is

- Simple definition: Flink processes continuous streams of data.
- Technical definition: Apache Flink is a distributed stream processing framework for stateful computations over bounded and unbounded data streams, with strong support for event time, checkpoints, and exactly-once state consistency.
- Category: Stream processing engine.
- Related terms: stream, state, checkpoint, watermark, window, operator, job.

## 4. Why It Exists

Kafka stores events, but does not by itself compute complex results.

Teams need:

- real-time aggregations
- fraud detection
- windowed metrics
- event-time correctness
- stateful processing
- low-latency pipelines
- failure recovery with state

Flink exists for serious continuous processing.

## 5. Where It Fits In A Data Platform

```text
Kafka / files / CDC
  -> Flink
  -> Kafka / database / data lake / dashboards / feature store
```

Flink is a processing layer.

## 6. How It Works Step By Step

1. Flink job starts.
2. Sources read events.
3. Operators transform/filter/join/window events.
4. Keyed state stores per-key information.
5. Watermarks track event-time progress.
6. Checkpoints save state consistently.
7. Sinks write results.
8. On failure, job restores from checkpoint.

## 7. How To Use It Practically

Common use cases:

- count events per minute
- detect fraud patterns
- enrich events
- join streams
- update real-time dashboards
- process CDC

Conceptual code:

```text
source(Kafka)
  -> filter valid events
  -> keyBy(user_id)
  -> window(5 minutes)
  -> aggregate
  -> sink(Kafka/table)
```

## 8. Real-World Scenario

- Product/system: Real-time fraud detection.
- Problem: Need to detect suspicious payment behavior within seconds.
- How Flink helps: Maintains per-user state and evaluates events continuously.
- What would go wrong without it: batch processing would detect fraud too late.

## 9. System Design Angle

Choose Flink when:

- low-latency streaming matters
- stateful processing is needed
- event-time correctness matters
- late events must be handled
- exactly-once state consistency is important

Avoid Flink when:

- daily batch is enough
- simple Kafka topic-to-topic transformation can use Kafka Streams
- team cannot operate streaming complexity

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| low-latency stream processing | operational complexity |
| strong state support | state backend tuning |
| event-time/window correctness | watermark design |
| checkpoint recovery | checkpoint overhead |

## 11. Failure Modes

- Failure: checkpoint failures.
- Symptom: job may not have recent recovery point.
- Recovery: fix storage/backpressure.
- Prevention: monitor checkpoints.

- Failure: state grows too large.
- Symptom: slow checkpoints and high storage.
- Recovery: TTL/cleanup/state redesign.
- Prevention: state sizing.

- Failure: watermark stuck.
- Symptom: windows do not close.
- Recovery: debug idle sources/event time.
- Prevention: watermark strategy and idleness handling.

## 12. Common Mistakes

- Mistake: Thinking Flink is a message broker.
- Why it is wrong: Kafka stores streams; Flink processes them.
- Better approach: separate storage/broker from processing engine.

- Mistake: Ignoring state size.
- Why it is wrong: state affects memory, checkpoint time, and recovery.
- Better approach: design state carefully.

## 13. Mini Example

```text
Kafka payments -> Flink fraud rules -> suspicious_payments topic
```

## 14. Interview Questions

1. What is Apache Flink?
2. Kafka vs Flink?
3. Why is Flink good for stateful streaming?
4. What are checkpoints?
5. What are watermarks?

## 15. Interview Speak

"Flink is a distributed stream processing engine. Kafka stores event streams, while Flink processes them continuously with state, event-time semantics, watermarks, windows, and checkpoints. I would choose Flink for low-latency stateful streaming, fraud detection, real-time analytics, and event-time correctness."

## 16. Quick Recall

- One-line summary: Flink continuously processes streams with state and event time.
- Three keywords: state, checkpoint, watermark.
- One trap: Confusing Flink with Kafka.
- One memory trick: Kafka is the river; Flink is the waterwheel doing work.
