# Phase 2 Review: Distributed Systems Foundations

This review checks whether the distributed-systems ideas are ready for Big Data system design.

## Phase Summary

Phase 2 covered the core patterns behind distributed storage, processing, messaging, and serving systems:

- distributing work across nodes
- copying data through replication
- splitting data through partitioning
- coordinating through leaders, quorum, and consensus
- surviving failure through retries, idempotency, backpressure, circuit breakers, and failover
- improving performance with load balancing, caching, and Bloom filters
- handling time, ordering, delivery semantics, eventual consistency, and distributed locks

Main idea:

```text
Distributed systems trade simple local correctness for scale, availability, and parallelism.
```

## Checkpoint 1: Topics 040-044

Topics:

- Distributed systems
- Replication
- Partitioning/sharding
- Consistent hashing
- Leader/follower architecture

### Quiz

1. Why do Big Data systems use multiple machines?
2. What does replication improve?
3. What makes a partition key good?
4. Why is consistent hashing better than modulo hashing for dynamic clusters?
5. What is replication lag?

### Practical Exercise

Design data placement for a clickstream store:

- choose replication factor
- choose partition key
- explain how reads and writes route
- identify one hot partition risk
- explain how a node failure is handled

### Mini System Design Question

> You are designing a distributed cache for user profiles. How would you distribute keys and handle adding new cache nodes?

Strong direction:

- Use consistent hashing.
- Use virtual nodes for balance.
- Replicate hot keys or use local cache if needed.
- Monitor cache hit rate and node load.

### Recap Table

| Concept | Must Remember |
|---|---|
| Distributed system | many nodes acting as one service |
| Replication | copies for availability/durability |
| Partitioning | split data for scale |
| Consistent hashing | less reshuffling when nodes change |
| Leader/follower | leader writes, followers copy |

## Checkpoint 2: Topics 045-049

Topics:

- Quorum
- Consensus basics
- Raft and Paxos intuition
- Fault tolerance
- Idempotency

### Quiz

1. What does `R + W > N` try to achieve?
2. Why does consensus usually need a majority?
3. What does Raft use a leader for?
4. Why is retry without idempotency dangerous?
5. What state does a recovering data pipeline need to know?

### Practical Exercise

Take a Kafka consumer pipeline and define:

- input topic
- event id
- processing state
- output table
- retry behavior
- deduplication strategy
- offset commit rule

### Mini System Design Question

> A payment API times out after charging the card but before returning a response. The client retries. How do you avoid double charge?

Strong direction:

- Use idempotency key.
- Store operation result by key.
- Retry returns original result.
- Make downstream payment call safe or reconcile by transaction id.

### Recap Table

| Concept | Must Remember |
|---|---|
| Quorum | enough replicas agree |
| Consensus | safe agreement under failure |
| Raft | leader election + replicated log |
| Fault tolerance | useful behavior despite failure |
| Idempotency | repeat attempts are safe |

## Checkpoint 3: Topics 050-054

Topics:

- Retries and exponential backoff
- Circuit breakers
- Backpressure
- Load balancing
- Caching

### Quiz

1. Why add jitter to retries?
2. What are the three circuit breaker states?
3. What does consumer lag tell you?
4. Why do load balancers need health checks?
5. What is a cache stampede?

### Practical Exercise

Design an API ingestion worker that:

- handles `429`
- retries with exponential backoff and jitter
- stops after max attempts
- writes failed records to a dead letter queue
- uses circuit breaker behavior when the API is down
- tracks backlog

### Mini System Design Question

> A dashboard service calls a slow metrics backend. During traffic spikes, the backend times out and the dashboard becomes unavailable. What do you change?

Strong direction:

- Add cache with TTL.
- Add timeouts.
- Add circuit breaker.
- Return stale data if acceptable.
- Add load balancing and health checks.
- Monitor latency and error rate.

### Recap Table

| Concept | Must Remember |
|---|---|
| Retry | recover transient failure |
| Backoff | avoid hammering dependency |
| Circuit breaker | fail fast when dependency is unhealthy |
| Backpressure | slow intake under overload |
| Load balancing | spread traffic across healthy nodes |
| Cache | reduce latency and backend load |

## Checkpoint 4: Topics 055-060

Topics:

- Bloom filters
- Clock skew
- Delivery semantics
- Ordering guarantees
- Eventual consistency
- Distributed locks

### Quiz

1. What can a Bloom filter say with certainty?
2. Why are client timestamps dangerous?
3. What is the difference between at-least-once and at-most-once?
4. What ordering does Kafka guarantee?
5. Why do distributed locks need fencing tokens?

### Practical Exercise

For each system, choose delivery and ordering guarantees:

- payment ledger
- clickstream analytics
- email notification service
- user profile updates
- CDC from database to lakehouse

### Mini System Design Question

> You are consuming CDC events from a database into a lakehouse table. What ordering and delivery issues must you handle?

Strong direction:

- Preserve per-primary-key order.
- Handle at-least-once duplicates.
- Use operation timestamps or log sequence numbers.
- Use idempotent merge/upsert.
- Monitor lag.
- Reconcile from source snapshots when needed.

### Recap Table

| Concept | Must Remember |
|---|---|
| Bloom filter | definitely no, maybe yes |
| Clock skew | machines disagree on time |
| At-least-once | duplicates possible |
| Ordering | usually per partition/key |
| Eventual consistency | stale now, converge later |
| Distributed lock | exclusive coordination with leases/fencing |

## Must-Know Concepts

You should be comfortable explaining:

- partial failure
- replication lag
- shard key choice
- hot partitions
- consistent hashing
- leader/follower failover
- quorum reads and writes
- consensus vs normal replication
- idempotency keys
- retry storms
- backpressure and consumer lag
- circuit breaker states
- cache invalidation and stampede
- Bloom filter false positives
- event time vs processing time
- at-least-once duplicate handling
- partition-level ordering
- eventual consistency with reconciliation
- distributed lock fencing

## Common Interview Questions

1. Why are distributed systems hard?
2. How would you choose a partition key?
3. What is replication lag and how do you handle it?
4. Explain consistent hashing and virtual nodes.
5. What is quorum and how does `R + W > N` help?
6. When would you use consensus?
7. How do retries cause duplicate writes?
8. How do you handle Kafka consumer lag?
9. How do you prevent cache stampede?
10. Explain at-least-once vs exactly-once.
11. How do you preserve event ordering?
12. Why are distributed locks risky?

## Hands-On Project

Build a mini resilient event processor.

### Requirements

Simulate input events with fields:

```text
event_id, user_id, sequence_number, event_type, created_at
```

### Steps

1. Partition events by `user_id`.
2. Simulate duplicate events.
3. Deduplicate by `event_id`.
4. Preserve order by `sequence_number` per user.
5. Retry failed processing with exponential backoff.
6. Quarantine permanently failed events.
7. Track processed offsets or sequence numbers.
8. Print final per-user event counts.

### What This Teaches

- partitioning
- ordering
- duplicates
- idempotency
- retries
- failure handling
- replay

## Production Checklist

Before designing a distributed data system, ask:

- What is partitioned?
- What is replicated?
- What is the replication factor?
- What is the partition key?
- Can partitions become hot?
- What consistency is required?
- Can reads be stale?
- What delivery semantics are acceptable?
- Can events be duplicated?
- Can events arrive out of order?
- What is the retry policy?
- Are operations idempotent?
- What happens under dependency failure?
- Is there backpressure?
- What happens when queues grow?
- Is caching safe?
- What is the TTL?
- What happens when a node fails?
- How does failover work?
- Is consensus needed?
- Are locks avoidable?
- If locks are used, are there fencing tokens?

## Final Phase 2 Interview Answer

"For distributed systems, I start by identifying data placement, replication, partitioning, and failure behavior. I expect partial failure, retries, duplicates, stale reads, and out-of-order events. I choose partition keys carefully, replicate for availability, use quorum or consensus only where correctness requires it, and design consumers to be idempotent. I protect systems with timeouts, exponential backoff with jitter, circuit breakers, backpressure, load balancing, and monitoring. For performance I use caching and data-skipping techniques, but I always state the consistency and freshness trade-offs."
