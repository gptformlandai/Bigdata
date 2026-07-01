# Topic 045: Quorum

## Goal

Understand quorum as a way to make distributed reads and writes agree across replicas.

## Simple Explanation

A quorum means "enough nodes agree."

Instead of waiting for every replica, a system can require a majority or configured number of replicas.

## Core Idea

- Definition: Quorum is the minimum number of replicas that must participate in a read or write for it to be accepted.
- Why it matters: It balances consistency, availability, and latency.
- Related terms: read quorum, write quorum, majority, replica factor, stale read.

## Basic Formula

For `N` replicas:

```text
R + W > N
```

Where:

- `R` = replicas required for read
- `W` = replicas required for write
- `N` = total replicas

If `R + W > N`, reads and writes overlap on at least one replica, increasing chance of seeing latest data.

## Example

Replication factor:

```text
N = 3
```

Common choices:

| R | W | Behavior |
|---:|---:|---|
| 1 | 1 | fastest, weakest consistency |
| 1 | 2 | faster reads, stronger writes |
| 2 | 1 | stronger reads, faster writes |
| 2 | 2 | quorum read/write |
| 3 | 3 | strongest, least available |

## Big Data / System Design Angle

Quorum appears in:

- Cassandra-style databases
- Dynamo-style systems
- consensus protocols
- leader election
- replicated metadata

Trade-offs:

- larger quorum improves consistency
- smaller quorum improves latency and availability
- quorum does not solve all conflicts by itself

## Common Mistakes

- Mistake: Thinking quorum always means strong consistency.
- Better way: Mention timing, conflicts, read repair, and protocol details.

- Mistake: Setting all operations to require all replicas.
- Better way: Balance correctness with availability and latency.

- Mistake: Ignoring tail latency.
- Better way: Waiting for more replicas can make p99 latency worse.

## Interview Speak

"Quorum requires a minimum number of replicas to acknowledge reads or writes. With `R + W > N`, read and write quorums overlap, improving consistency. The trade-off is latency and availability: larger quorums are safer but slower and less tolerant of failures."

## Quick Recall

- One-liner: Quorum means enough replicas agree.
- Keywords: R, W, N.
- Trap: Saying quorum automatically guarantees perfect consistency in every system.
