# Topic 110: Kafka Broker

## 1. Goal

Understand brokers as Kafka servers that store and serve topic partitions.

## 2. Baby Intuition

A Kafka broker is like one library branch in a library system.

It stores some shelves of books, serves readers, accepts new books, and coordinates with other branches.

## 3. What It Is

- Simple definition: A broker is a Kafka server.
- Technical definition: A Kafka broker stores partition log segments, handles producer writes and consumer reads, participates in replication, and serves metadata to clients.
- Category: Kafka cluster component.
- Related terms: cluster, partition leader, replica, controller, log segment, broker id.

## 4. Why It Exists

Kafka needs many servers because one machine cannot handle unlimited:

- events
- storage
- network traffic
- consumers
- producers
- availability requirements

Brokers let Kafka scale horizontally.

## 5. Where It Fits In A Data Platform

```text
Producers -> Kafka brokers -> Consumers
```

A Kafka cluster is a group of brokers.

## 6. How It Works Step By Step

1. Broker starts with unique broker id.
2. It joins Kafka cluster.
3. Some topic partitions are assigned to it.
4. For some partitions, it may be leader.
5. Producers write to partition leaders.
6. Followers replicate from leaders.
7. Consumers fetch from leaders.
8. Broker stores partition data as log files.

## 7. How To Use It Practically

Operational things to monitor:

- broker disk usage
- network in/out
- request latency
- under-replicated partitions
- offline partitions
- controller health
- leader distribution

Broker config examples:

```properties
broker.id=1
log.dirs=/kafka-logs
num.network.threads=3
num.io.threads=8
```

## 8. Real-World Scenario

- Product/system: Company event platform.
- Problem: Millions of events per second need durable storage.
- How brokers help: Many brokers share partitions and traffic.
- What would go wrong without brokers: one machine would be overloaded and a single failure could stop ingestion.

## 9. System Design Angle

Broker count affects:

- throughput
- storage capacity
- fault tolerance
- partition placement
- cost

Design questions:

- how much data per day?
- retention period?
- replication factor?
- partitions per broker?
- peak throughput?

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| horizontal scale | cluster operations |
| storage distribution | rebalancing complexity |
| fault tolerance | replication network cost |
| more throughput | more monitoring |

## 11. Failure Modes

- Failure: broker disk full.
- Symptom: produce failures or broker crash.
- Recovery: add storage/delete data/fix retention.
- Prevention: disk alerts and retention planning.

- Failure: broker down.
- Symptom: partition leaders move if replicas exist.
- Recovery: restart broker or replace node.
- Prevention: replication factor and ISR monitoring.

## 12. Common Mistakes

- Mistake: Thinking every broker stores every topic.
- Why it is wrong: brokers store assigned partitions/replicas.
- Better approach: think partition placement.

- Mistake: Ignoring disk.
- Why it is wrong: Kafka is storage-heavy.
- Better approach: monitor disk and retention.

## 13. Mini Example

```text
Broker 1: orders-0 leader, payments-1 follower
Broker 2: orders-1 leader, orders-0 follower
Broker 3: orders-2 leader, payments-0 leader
```

## 14. Interview Questions

1. What is a Kafka broker?
2. What does a broker store?
3. What happens if a broker fails?
4. How do brokers scale Kafka?
5. What broker metrics matter?

## 15. Interview Speak

"A Kafka broker is a server in the Kafka cluster. Brokers store partition logs, handle producer and consumer requests, and replicate partition data. Topics are split into partitions distributed across brokers, which gives Kafka horizontal scalability and fault tolerance."

## 16. Quick Recall

- One-line summary: Broker is a Kafka server storing partition logs.
- Three keywords: broker, partition, replica.
- One trap: Thinking each broker stores everything.
- One memory trick: Broker is one branch in the Kafka library.
