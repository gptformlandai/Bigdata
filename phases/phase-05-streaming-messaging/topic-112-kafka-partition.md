# Topic 112: Kafka Partition

## 1. Goal

Understand partitions as Kafka's unit of parallelism, ordering, and storage distribution.

## 2. Baby Intuition

A topic is a highway.

Partitions are lanes.

More lanes allow more cars to move in parallel, but order is only guaranteed inside one lane.

## 3. What It Is

- Simple definition: A partition is an ordered log inside a topic.
- Technical definition: A Kafka partition is an append-only ordered sequence of records, stored on brokers and identified by monotonically increasing offsets.
- Category: Kafka scalability and ordering unit.
- Related terms: offset, key, leader, replica, consumer group.

## 4. Why It Exists

One topic on one machine would limit:

- throughput
- storage
- consumer parallelism
- fault distribution

Partitions let Kafka split one topic across brokers and consumers.

## 5. Where It Fits In A Data Platform

```text
Topic
  -> partition 0
  -> partition 1
  -> partition 2
```

Consumers in a group divide partitions among themselves.

## 6. How It Works Step By Step

1. Producer sends record to topic.
2. Kafka chooses partition.
3. If key is provided, key hash usually determines partition.
4. Record is appended to partition log.
5. Record gets an offset within that partition.
6. Consumers read records in partition order.

## 7. How To Use It Practically

Create topic with partitions:

```bash
kafka-topics --bootstrap-server localhost:9092 --create --topic orders --partitions 6 --replication-factor 3
```

Increase partitions:

```bash
kafka-topics --bootstrap-server localhost:9092 --alter --topic orders --partitions 12
```

Warning:

```text
Increasing partitions can change key-to-partition mapping for new records.
```

## 8. Real-World Scenario

- Product/system: Payment event stream.
- Problem: Need high throughput and per-payment ordering.
- How partitions help: Partition by payment id or account id depending on ordering need.
- What would go wrong without it: one partition becomes bottleneck.

## 9. System Design Angle

Partitions affect:

- throughput
- ordering
- consumer parallelism
- rebalancing
- broker load
- storage distribution

Partition key must match ordering requirement.

Example:

```text
Need order per user -> key by user_id
Need order per order -> key by order_id
```

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| parallelism | no global order |
| higher throughput | partition count planning |
| broker distribution | rebalancing overhead |
| per-key ordering | hot key risk |

## 11. Failure Modes

- Failure: hot partition.
- Symptom: one broker/consumer overloaded.
- Recovery: change key strategy or split hot key.
- Prevention: inspect key distribution.

- Failure: too few partitions.
- Symptom: limited consumer parallelism.
- Recovery: increase partitions.
- Prevention: estimate throughput and consumers.

## 12. Common Mistakes

- Mistake: Expecting global order across topic.
- Why it is wrong: Kafka orders records only within a partition.
- Better approach: key events that require ordering into same partition.

- Mistake: Over-partitioning blindly.
- Why it is wrong: more metadata, file handles, rebalancing overhead.
- Better approach: size partitions for throughput and parallelism.

## 13. Mini Example

```text
orders topic:
partition 0: offsets 0, 1, 2
partition 1: offsets 0, 1, 2
partition 2: offsets 0, 1, 2
```

Offset 1 in partition 0 is different from offset 1 in partition 2.

## 14. Interview Questions

1. What is a Kafka partition?
2. How do partitions affect ordering?
3. How do partitions affect parallelism?
4. What is a hot partition?
5. Can you increase partition count?

## 15. Interview Speak

"A Kafka partition is an ordered append-only log within a topic. Partitions provide Kafka's scale and consumer parallelism, but ordering is only guaranteed within a partition. Choosing the partition key is important because it controls ordering and load distribution."

## 16. Quick Recall

- One-line summary: Partition is one ordered lane inside a topic.
- Three keywords: order, offset, parallelism.
- One trap: Assuming global topic order.
- One memory trick: Topic highway, partition lanes.
