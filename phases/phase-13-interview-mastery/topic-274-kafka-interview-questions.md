# Topic 274: Kafka Interview Questions

## 1. Goal

Prepare Kafka answers around topics, partitions, offsets, consumer groups, ordering, replication, delivery guarantees, and lag.

## 2. Baby Intuition

Kafka is a durable event log.

Producers append events. Consumers read events at their own pace using offsets.

## 3. Must-Know Kafka Concepts

- broker
- topic
- partition
- offset
- producer
- consumer
- consumer group
- replication factor
- leader/follower replica
- ISR
- acknowledgments
- retention
- compaction
- schema registry
- consumer lag

## 4. Common Questions And Strong Answers

| Question | Strong Answer |
|---|---|
| What is Kafka? | distributed durable event streaming platform |
| Topic vs partition? | topic is logical stream; partition is ordered shard |
| What is offset? | position of a message within a partition |
| Consumer group? | consumers share partitions for parallel processing |
| Kafka ordering? | guaranteed within a partition, not across partitions |

## 5. Producer Questions

Important settings:

- key
- acks
- retries
- idempotent producer
- batching
- compression

Strong line:

```text
The message key controls partitioning, so it controls ordering and load distribution.
```

## 6. Consumer Questions

Consumer group behavior:

- each partition is consumed by only one consumer in a group
- adding consumers increases parallelism up to partition count
- offsets track progress
- rebalances move partitions between consumers

Lag means:

```text
latest produced offset - committed consumed offset
```

## 7. Delivery Semantics Questions

| Semantic | Meaning |
|---|---|
| at-most-once | may lose messages, no duplicates |
| at-least-once | no loss if configured, duplicates possible |
| exactly-once effect | output behaves once through transactions/idempotency |

Interview maturity:

```text
In practice, I design consumers idempotently because retries and duplicates can happen.
```

## 8. Ordering Questions

Kafka guarantees order only inside one partition.

If you need order per user/order:

- choose key = user_id or order_id
- all events for that key go to same partition
- accept that global ordering is not guaranteed

Trade-off:

```text
more ordering constraint can reduce parallelism and create hot keys
```

## 9. Retention And Compaction

Retention:

- keep events for time/size window
- useful for replay

Compaction:

- keep latest value per key
- useful for changelog/current-state topics

## 10. Failure And Lag Questions

Consumer lag causes:

- consumers too slow
- too few partitions/consumers
- downstream database slow
- message burst
- rebalance instability
- bad processing logic

Debug steps:

1. Check lag by topic/partition.
2. Check consumer errors and processing latency.
3. Check downstream sink.
4. Scale consumers if partitions allow.
5. Optimize processing or add partitions for future scale.

## 11. Schema Questions

Schema Registry helps:

- enforce compatible schemas
- prevent breaking consumers
- version event contracts

Good event design:

- stable key
- event_id
- event_time
- schema version
- avoid huge payloads

## 12. Practical Interview Questions

1. How does Kafka scale?
2. How does Kafka preserve ordering?
3. What is consumer lag?
4. How do you handle duplicate events?
5. What is ISR?
6. What is compaction?
7. How would you design Kafka for CDC?
8. What happens during rebalance?

## 13. Sample Strong Answer

Question:

```text
Kafka consumer lag is growing. What do you check?
```

Answer:

```text
I check lag by partition to see whether the issue is global or a hot partition. Then I inspect consumer processing latency, errors, rebalances, and downstream sink latency. If consumers are CPU-bound and partition count allows it, I scale the consumer group. If one partition is hot, I revisit key distribution. I also verify batch size, commit behavior, and whether a recent schema or code change increased processing time.
```

## 14. Quick Recall

- One-line summary: Kafka is an ordered per-partition event log with replay.
- Three keywords: partitions, offsets, consumer groups.
- One trap: promising global ordering.
- Memory trick: many durable queues called partitions.

