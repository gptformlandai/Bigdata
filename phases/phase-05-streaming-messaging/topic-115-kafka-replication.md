# Topic 115: Kafka Replication

## 1. Goal

Understand Kafka replication as copying partition data across brokers for fault tolerance.

## 2. Baby Intuition

If one notebook is important, keep copies in different rooms.

Kafka keeps copies of partition logs on multiple brokers.

## 3. What It Is

- Simple definition: Replication keeps copies of partition data on multiple brokers.
- Technical definition: Kafka replicates each partition across brokers according to replication factor, with one leader replica and follower replicas.
- Category: Kafka durability and availability.
- Related terms: leader, follower, replica, ISR, replication factor, failover.

## 4. Why It Exists

Brokers fail.

Replication prevents one broker failure from losing or stopping access to partition data.

It helps with:

- durability
- availability
- broker maintenance
- leader failover

## 5. Where It Fits In A Data Platform

```text
topic partition -> leader replica + follower replicas on brokers
```

Producers and consumers talk to leaders. Followers copy from leaders.

## 6. How It Works Step By Step

Replication factor 3:

1. Partition has 3 replicas.
2. One replica is leader.
3. Two replicas are followers.
4. Producer writes to leader.
5. Followers fetch data from leader.
6. If leader fails, Kafka elects new leader from in-sync replicas.

## 7. How To Use It Practically

Create replicated topic:

```bash
kafka-topics --bootstrap-server localhost:9092 --create --topic payments --partitions 6 --replication-factor 3
```

Describe:

```bash
kafka-topics --bootstrap-server localhost:9092 --describe --topic payments
```

Look for:

- Leader
- Replicas
- Isr

## 8. Real-World Scenario

- Product/system: Payment event stream.
- Problem: Broker failure must not lose payment events.
- How replication helps: Partition replicas exist on other brokers.
- What would go wrong without it: broker loss could lose data or stop partition access.

## 9. System Design Angle

Replication factor affects:

- durability
- availability
- storage cost
- network traffic
- write latency depending on acks

Common production default:

```text
replication factor = 3
```

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| tolerate broker failure | more storage |
| leader failover | replication traffic |
| better durability | possible write latency |
| maintenance flexibility | ISR monitoring needed |

## 11. Failure Modes

- Failure: followers fall behind.
- Symptom: ISR shrinks.
- Recovery: follower catches up or broker fixed.
- Prevention: monitor under-replicated partitions.

- Failure: all replicas unavailable.
- Symptom: partition offline.
- Recovery: restore brokers.
- Prevention: rack-aware placement and replication.

## 12. Common Mistakes

- Mistake: replication factor 1 for important topics.
- Why it is wrong: no broker failure tolerance.
- Better approach: use RF 3 for important production topics.

- Mistake: thinking replication replaces backups.
- Why it is wrong: bad deletes/configs can still affect cluster.
- Better approach: plan retention, mirroring, or backups where needed.

## 13. Mini Example

```text
orders-0:
leader: broker 1
followers: broker 2, broker 3
```

## 14. Interview Questions

1. What is Kafka replication?
2. What is replication factor?
3. What are leader and follower replicas?
4. What happens when leader fails?
5. How does replication affect cost?

## 15. Interview Speak

"Kafka replication copies partition logs across brokers. Each partition has one leader and follower replicas. Producers and consumers interact with the leader, while followers replicate from it. If the leader fails, Kafka can elect a new leader from in-sync replicas, improving availability and durability."

## 16. Quick Recall

- One-line summary: Replication keeps partition copies on multiple brokers.
- Three keywords: leader, follower, ISR.
- One trap: RF 1 for critical data.
- One memory trick: Important notebook has copies.
