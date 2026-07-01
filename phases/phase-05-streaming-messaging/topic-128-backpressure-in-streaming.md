# Topic 128: Backpressure In Streaming

## 1. Goal

Understand backpressure as how streaming systems protect themselves when input is faster than processing.

## 2. Baby Intuition

If water enters a pipe faster than it can drain, the pipe overflows.

Backpressure is the system controlling flow before it bursts.

## 3. What It Is

- Simple definition: Backpressure slows or limits intake when consumers cannot keep up.
- Technical definition: Backpressure is flow-control behavior that prevents streaming pipelines from being overwhelmed by producer rate, processing bottlenecks, or slow sinks.
- Category: Streaming reliability pattern.
- Related terms: lag, throttling, rate limiting, buffer, queue, checkpoint, sink bottleneck.

## 4. Why It Exists

Streaming systems are continuous.

If input rate > processing rate:

```text
backlog grows forever
```

Eventually:

- memory fills
- lag grows
- latency increases
- consumers crash
- downstream systems get overloaded

## 5. Where It Fits In A Data Platform

```text
Kafka -> stream processor -> sink
          ^
      backpressure
```

Backpressure can happen at:

- producer
- broker
- consumer
- stream processor
- database/sink

## 6. How It Works Step By Step

1. Processor reads events.
2. Processing or sink slows.
3. Internal buffers fill or lag grows.
4. System reduces read rate, pauses intake, or applies throttling.
5. Backlog stabilizes.
6. Once healthy, processing catches up.

## 7. How To Use It Practically

Signals:

- Kafka consumer lag grows
- processing time > batch interval
- queue depth grows
- sink write latency increases
- memory pressure rises

Mitigations:

- scale consumers
- increase partitions
- optimize processing
- batch sink writes
- throttle producers
- shed low-priority data
- tune max poll/read rates

## 8. Real-World Scenario

- Product/system: Real-time metrics pipeline.
- Problem: Database sink slows during peak traffic.
- How backpressure helps: Consumer reads less from Kafka instead of crashing.
- What would go wrong without it: memory grows, retries spike, and pipeline fails.

## 9. System Design Angle

Backpressure is required for stable real-time systems.

Ask:

- what is max input rate?
- what is max processing rate?
- what is sink throughput?
- where can buffering happen?
- what is acceptable lag?
- what happens under sustained overload?

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| stability under overload | increased lag |
| protects sinks | slower freshness |
| prevents crashes | possible data shedding |
| controlled recovery | tuning complexity |

## 11. Failure Modes

- Failure: unbounded buffers.
- Symptom: memory OOM.
- Recovery: restart and reduce rate.
- Prevention: bounded queues/backpressure.

- Failure: slow sink.
- Symptom: lag grows despite healthy Kafka.
- Recovery: optimize/scale sink.
- Prevention: sink capacity planning.

## 12. Common Mistakes

- Mistake: Treating Kafka retention as infinite buffer.
- Why it is wrong: retention can expire backlog.
- Better approach: size retention and processing capacity.

- Mistake: Scaling consumers without checking sink.
- Why it is wrong: sink may be bottleneck.
- Better approach: identify bottleneck first.

## 13. Mini Example

```text
input rate: 50,000 events/sec
processing rate: 30,000 events/sec
backlog growth: 20,000 events/sec
```

This needs scaling, throttling, or optimization.

## 14. Interview Questions

1. What is backpressure?
2. How does lag relate to backpressure?
3. What causes backpressure?
4. How do you handle slow sinks?
5. What happens without backpressure?

## 15. Interview Speak

"Backpressure is flow control that keeps streaming systems stable when input exceeds processing or sink capacity. I watch lag, processing time, queue depth, and sink latency, then scale consumers, optimize processing, batch writes, throttle producers, or shed low-priority load as needed."

## 16. Quick Recall

- One-line summary: Backpressure slows intake to protect the pipeline.
- Three keywords: lag, throttle, sink.
- One trap: Scaling consumers when sink is the bottleneck.
- One memory trick: Do not pour faster than the drain.
