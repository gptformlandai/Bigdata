# Topic 017: CAP Theorem

## Goal

Understand CAP theorem without the common oversimplifications, and know how to use it in system design conversations.

## Simple Explanation

CAP says a distributed system cannot always guarantee all three at the same time:

- Consistency
- Availability
- Partition tolerance

The key situation is a network partition. When machines cannot reliably talk to each other, the system must choose what to protect: latest correct data or continued responses.

## Core Idea

- Definition: During a network partition, a distributed system must choose between consistency and availability.
- Why it matters: Distributed data systems run across machines, and networks fail.
- Related terms: CP, AP, partition, quorum, replication, eventual consistency.

## The Three Letters

| Letter | Meaning | Simple Version |
|---|---|---|
| C | Consistency | every read sees the latest write |
| A | Availability | every request receives a non-error response |
| P | Partition tolerance | system continues despite network splits |

Important nuance:

Partition tolerance is not optional in real distributed systems. Networks can fail. So the real trade-off during a partition is usually:

```text
CP or AP?
```

## CP vs AP

CP system:

- protects consistency during partition
- may reject or delay requests
- example use cases: locks, metadata, financial correctness

AP system:

- keeps serving during partition
- may return stale or conflicting data
- example use cases: feeds, likes, shopping carts, some caches

## Big Data / System Design Angle

CAP appears when designing:

- distributed databases
- replicated storage
- metadata systems
- caches
- event stores
- distributed locks
- multi-region systems

Interview trigger words:

- multi-region
- replicated database
- network partition
- consistency vs availability
- stale reads
- quorum

## Example

Imagine user profile data replicated in two regions.

```text
Region A cannot talk to Region B.
```

If user updates profile in Region A:

- CP choice: Region B refuses reads/writes until it can confirm latest state.
- AP choice: Region B continues serving, possibly with stale profile data.

Neither is always right. The business requirement decides.

## Common Mistakes

- Mistake: Saying a system "chooses two of three" permanently.
- Better way: Say during a partition, the system chooses consistency or availability.

- Mistake: Treating availability as "fast response."
- Better way: CAP availability means every non-failing node returns a non-error response.

- Mistake: Using CAP for single-node databases.
- Better way: CAP is about distributed systems under partition.

## Interview Speak

"CAP is mainly about what happens during a network partition. Since partitions can happen in distributed systems, the practical decision is whether we prefer consistency or availability during that failure. For payments I would lean CP; for social likes or feeds I may accept AP with reconciliation."

## Quick Recall

- One-liner: During network partition, choose latest correctness or continued service.
- Keywords: partition, CP, AP.
- Trap: Saying "pick any two" without explaining the partition scenario.
