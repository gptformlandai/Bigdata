# Phase 2: Distributed Systems Foundations

Phase 2 explains the ideas that make Big Data systems work across many machines.

This phase is more system-design heavy than Phase 0. The notes are still modular, but topics like replication, partitioning, consensus, fault tolerance, idempotency, backpressure, ordering, and distributed locks deserve deeper trade-off thinking.

## Topics

| # | Topic | Status |
|---:|---|---|
| 040 | Distributed systems | Complete |
| 041 | Replication | Complete |
| 042 | Partitioning/sharding | Complete |
| 043 | Consistent hashing | Complete |
| 044 | Leader/follower architecture | Complete |
| 045 | Quorum | Complete |
| 046 | Consensus basics | Complete |
| 047 | Raft and Paxos intuition | Complete |
| 048 | Fault tolerance | Complete |
| 049 | Idempotency | Complete |
| 050 | Retries and exponential backoff | Complete |
| 051 | Circuit breakers | Complete |
| 052 | Backpressure | Complete |
| 053 | Load balancing | Complete |
| 054 | Caching | Complete |
| 055 | Bloom filters | Complete |
| 056 | Clock skew | Complete |
| 057 | Exactly-once vs at-least-once vs at-most-once | Complete |
| 058 | Ordering guarantees | Complete |
| 059 | Eventual consistency | Complete |
| 060 | Distributed locks | Complete |

## Phase Goal

By the end of this phase, you should be able to explain:

- why systems are distributed
- how data is replicated and partitioned
- how systems coordinate through leaders, quorum, and consensus
- how failure is expected and handled
- how retries, idempotency, circuit breakers, and backpressure protect systems
- how load balancing, caching, bloom filters, clocks, delivery semantics, ordering, eventual consistency, and locks affect real architectures

## Suggested Study Flow

1. Read Topics 040-046 for distributed data placement and coordination basics.
2. Read Topics 047-053 for failure handling and traffic control.
3. Read Topics 054-060 for performance, correctness, and advanced guarantees.
4. Finish with `phase-02-review.md`.
