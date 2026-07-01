# Topic 114: Kafka Consumer Group

## 1. Goal

Understand consumer groups as Kafka's way to scale consumers and let different applications read independently.

## 2. Baby Intuition

A consumer group is a team reading a topic.

Each partition is assigned to one team member at a time. Another team can read the same topic independently.

## 3. What It Is

- Simple definition: A consumer group is a set of consumers sharing work for subscribed partitions.
- Technical definition: Kafka assigns partitions of subscribed topics among consumers in the same group, while each group tracks its own offsets independently.
- Category: Kafka consumption parallelism.
- Related terms: consumer, partition assignment, rebalance, offset commit, lag.

## 4. Why It Exists

Kafka needs two patterns:

1. Scale one application with multiple workers.
2. Let multiple applications read same events independently.

Consumer groups solve both.

## 5. Where It Fits In A Data Platform

```text
orders topic
  -> fraud-consumer-group
  -> analytics-consumer-group
  -> data-lake-consumer-group
```

Each group has its own offsets.

## 6. How It Works Step By Step

1. Consumers join a group.
2. Group coordinator assigns partitions.
3. Each partition is consumed by at most one consumer in the group.
4. Consumers process records.
5. Consumers commit offsets.
6. If a consumer joins/leaves, rebalance happens.

## 7. How To Use It Practically

Consumer config:

```properties
group.id=analytics-workers
enable.auto.commit=false
```

Check group:

```bash
kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group analytics-workers
```

Rule:

```text
Max useful consumers in one group <= number of partitions.
```

If topic has 6 partitions, only 6 consumers can actively consume in that group.

## 8. Real-World Scenario

- Product/system: Order event platform.
- Problem: Fraud, analytics, and email systems all need order events.
- How groups help: Each application uses a separate group and tracks its own progress.
- What would go wrong without it: consumers would fight over messages or duplicate coordination logic.

## 9. System Design Angle

Consumer groups affect:

- scalability
- ordering
- lag
- failover
- rebalancing

Design questions:

- how many partitions?
- how many consumers?
- how fast can each consumer process?
- what happens during rebalance?

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| horizontal consumption | rebalancing complexity |
| independent applications | offset management |
| failover among consumers | max parallelism tied to partitions |
| per-group replay | duplicate handling needed |

## 11. Failure Modes

- Failure: consumer dies.
- Symptom: partitions reassigned after rebalance.
- Recovery: other consumers continue.
- Prevention: health checks and stable consumers.

- Failure: too few partitions.
- Symptom: extra consumers idle.
- Recovery: increase partitions if acceptable.
- Prevention: plan partition count.

- Failure: rebalance storm.
- Symptom: consumers repeatedly pause/reassign.
- Recovery: tune session timeouts and stability.
- Prevention: avoid unstable consumers.

## 12. Common Mistakes

- Mistake: Adding more consumers than partitions and expecting speedup.
- Why it is wrong: only one consumer per partition per group.
- Better approach: increase partitions or optimize consumers.

- Mistake: Using same group id for different applications.
- Why it is wrong: they share work instead of independently reading.
- Better approach: separate group ids per application.

## 13. Mini Example

```text
Topic has 3 partitions.
Group has 2 consumers.

consumer A -> partition 0, partition 1
consumer B -> partition 2
```

## 14. Interview Questions

1. What is a consumer group?
2. How are partitions assigned?
3. Why can extra consumers be idle?
4. What is rebalance?
5. Why use different group ids?

## 15. Interview Speak

"A Kafka consumer group is a set of consumers sharing partitions for an application. Each partition is consumed by only one consumer in the group at a time, and each group has independent offsets. Consumer groups provide horizontal scaling and failover, but parallelism is limited by partition count."

## 16. Quick Recall

- One-line summary: Consumer group is a team sharing partitions.
- Three keywords: group id, assignment, rebalance.
- One trap: More consumers than partitions.
- One memory trick: One partition, one team member at a time.
