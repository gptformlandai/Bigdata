# Topic 041: Replication

## Goal

Understand replication as copying data across machines for availability, durability, and read scalability.

## Simple Explanation

Replication means keeping copies of data on multiple machines.

If one copy fails, another copy can serve the data.

## Core Idea

- Definition: Replication stores the same data on multiple nodes or regions.
- Why it matters: It improves fault tolerance, durability, and read availability.
- Related terms: leader, follower, replica, synchronous replication, asynchronous replication, quorum, failover.

## Why Replicate

Replication helps with:

- surviving node failure
- reducing data loss risk
- increasing read capacity
- serving users closer to their region
- enabling maintenance without downtime

## Replication Styles

| Style | Meaning | Trade-off |
|---|---|---|
| Synchronous | write waits for replicas | stronger consistency, higher latency |
| Asynchronous | primary returns before all replicas catch up | lower latency, possible lag/data loss |
| Single leader | one node accepts writes | simpler ordering, leader bottleneck |
| Multi-leader | multiple nodes accept writes | better regional writes, conflict handling |
| Leaderless | clients write/read from multiple replicas | high availability, quorum complexity |

## How It Works

Typical leader/follower flow:

1. Client writes to leader.
2. Leader writes locally.
3. Leader sends change to followers.
4. Followers apply change.
5. Reads may go to leader or followers depending on consistency needs.

Failure path:

- leader fails
- system detects failure
- follower is promoted
- clients reconnect to new leader

## Big Data / System Design Angle

Replication factor is a key design number.

Example:

```text
Replication factor 3 = keep 3 copies of each data block/partition
```

Benefits:

- tolerate node failure
- improve read availability

Costs:

- more storage
- more network traffic
- replication lag
- failover complexity

## Common Mistakes

- Mistake: Thinking replicas are always identical instantly.
- Better way: Mention replication lag.

- Mistake: Reading from followers when strong consistency is required.
- Better way: Read from leader or use quorum/linearizable reads.

- Mistake: Ignoring failover behavior.
- Better way: Explain how a new leader is elected and how clients recover.

## Interview Speak

"Replication stores multiple copies of data to improve durability and availability. The trade-off is storage cost, network overhead, lag, and failover complexity. For strong consistency I may use synchronous replication or quorum reads/writes; for lower latency I may accept asynchronous replication and monitor lag."

## Quick Recall

- One-liner: Replication is copying data so failure does not mean loss.
- Keywords: replica, lag, failover.
- Trap: Assuming follower reads are always fresh.
