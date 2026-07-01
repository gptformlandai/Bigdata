# Topic 048: Fault Tolerance

## Goal

Understand how systems keep working when components fail.

## Simple Explanation

Fault tolerance means the system expects failure and continues operating.

Instead of asking "what if a node fails?", distributed systems ask "what do we do when a node fails?"

## Core Idea

- Definition: Fault tolerance is the ability to continue functioning despite hardware, software, network, or dependency failures.
- Why it matters: At scale, failures are constant.
- Related terms: redundancy, replication, failover, retry, timeout, circuit breaker, graceful degradation.

## What Can Fail

Common failures:

- node crash
- disk failure
- network timeout
- dependency outage
- bad deployment
- overloaded service
- corrupted data
- clock skew
- zone/region outage

## How Systems Tolerate Failure

Techniques:

- replication
- partitioning
- load balancing
- retries with backoff
- timeouts
- circuit breakers
- health checks
- failover
- data checkpointing
- dead letter queues
- graceful degradation
- backups and restore

## Big Data / System Design Angle

Big Data fault tolerance examples:

- Spark recomputes failed tasks using lineage.
- Kafka replicates partitions across brokers.
- Flink uses checkpoints.
- HDFS stores multiple block replicas.
- Airflow retries failed tasks.
- Data lakes keep raw immutable data for replay.

Important idea:

```text
Failure recovery needs state.
```

You need to know:

- what was processed
- what was committed
- what can be retried
- what may duplicate
- what must be reconciled

## Trade-offs

| Technique | Benefit | Cost |
|---|---|---|
| Replication | survive node loss | storage/network cost |
| Retry | recover transient failures | duplicate work/load amplification |
| Checkpoint | resume progress | overhead |
| Failover | availability | complexity |
| Graceful degradation | user impact reduced | incomplete functionality |

## Common Mistakes

- Mistake: Assuming retry equals fault tolerance.
- Better way: Retry with timeout, backoff, idempotency, and limits.

- Mistake: Ignoring recovery state.
- Better way: track offsets, checkpoints, commits, and idempotency keys.

- Mistake: Only designing happy path.
- Better way: describe failure path and recovery path.

## Interview Speak

"Fault tolerance means designing for expected failures. I would use redundancy, replication, timeouts, retries with backoff, idempotency, checkpointing, failover, and monitoring. For data systems, I care especially about what has been committed, what can be replayed, and how to avoid duplicates or data loss."

## Quick Recall

- One-liner: Fault tolerance means the system keeps useful behavior during failure.
- Keywords: redundancy, failover, recovery.
- Trap: Retrying without idempotency.
