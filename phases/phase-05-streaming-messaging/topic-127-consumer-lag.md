# Topic 127: Consumer Lag

## 1. Goal

Understand consumer lag as the distance between produced events and consumed progress.

## 2. Baby Intuition

Kafka is a conveyor belt.

Consumer lag means boxes are piling up because workers are behind.

## 3. What It Is

- Simple definition: Lag is how far behind a consumer is.
- Technical definition: Consumer lag is the difference between the latest offset in a partition and the consumer group's committed/current offset.
- Category: Kafka operations metric.
- Related terms: offset, log end offset, committed offset, consumer group, backpressure.

## 4. Why It Exists

Kafka decouples producers and consumers.

Producers can write faster than consumers read.

Lag measures that backlog.

## 5. Where It Fits In A Data Platform

```text
producer writes offsets -> consumer commits offsets -> lag = distance
```

Lag is monitored per:

```text
consumer group + topic + partition
```

## 6. How It Works Step By Step

Example:

```text
latest offset = 1000
consumer offset = 700
lag = 300
```

If lag grows over time:

```text
consumer cannot keep up
```

If lag shrinks:

```text
consumer is catching up
```

## 7. How To Use It Practically

Check lag:

```bash
kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group analytics
```

Common causes:

- consumer processing slow
- downstream database slow
- too few consumers
- too few partitions
- rebalance issues
- poison messages
- large spikes

## 8. Real-World Scenario

- Product/system: Real-time dashboard.
- Problem: Dashboard should be fresh within 2 minutes.
- How lag helps: Lag shows if stream processor is behind.
- What would go wrong without it: dashboard silently becomes stale.

## 9. System Design Angle

Lag affects freshness SLA.

Ask:

- how much lag is acceptable?
- is lag measured in records or time?
- can consumers scale?
- is downstream sink bottlenecked?
- is partition count enough?

## 10. Trade-offs

| Lower Lag | Higher Lag Tolerance |
|---|---|
| fresher outputs | fewer resources |
| better real-time UX | cheaper processing |
| faster alerts | more stale data |

## 11. Failure Modes

- Failure: lag grows beyond retention.
- Symptom: consumer offsets out of range.
- Recovery: reset offsets or restore from source.
- Prevention: retention sized for outages.

- Failure: one partition lagging.
- Symptom: skew/hot partition.
- Recovery: investigate key distribution.
- Prevention: good partition keys.

## 12. Common Mistakes

- Mistake: Looking only at total lag.
- Why it is wrong: one partition may be badly behind.
- Better approach: inspect per-partition lag.

- Mistake: Adding consumers when partitions are too few.
- Why it is wrong: extra consumers idle.
- Better approach: tune partitions or processing.

## 13. Mini Example

```text
partition 0: lag 10
partition 1: lag 20
partition 2: lag 500000
```

This suggests partition 2 or its assigned consumer is the problem.

## 14. Interview Questions

1. What is consumer lag?
2. How do you calculate lag?
3. What causes lag?
4. How do you reduce lag?
5. Why check per-partition lag?

## 15. Interview Speak

"Consumer lag is the difference between the latest Kafka offset and a consumer group's progress. It tells whether consumers are keeping up. I monitor lag per partition and investigate processing speed, downstream sinks, partition count, consumer count, skew, and rebalances."

## 16. Quick Recall

- One-line summary: Lag is unread backlog.
- Three keywords: offset, backlog, freshness.
- One trap: Only checking total lag.
- One memory trick: Boxes piling on conveyor belt.
