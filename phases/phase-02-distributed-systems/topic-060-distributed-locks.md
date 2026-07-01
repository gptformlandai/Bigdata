# Topic 060: Distributed Locks

## Goal

Understand distributed locks, when they are useful, and why they are dangerous if implemented casually.

## Simple Explanation

A distributed lock lets only one worker or service instance do something at a time across many machines.

Example:

```text
Only one scheduler should run the daily billing job.
```

## Core Idea

- Definition: A distributed lock coordinates exclusive access to a shared resource across multiple nodes.
- Why it matters: Some operations must not run concurrently.
- Related terms: lease, fencing token, TTL, consensus, ZooKeeper, etcd, Redis lock.

## When To Use

Useful for:

- leader election
- singleton scheduled jobs
- preventing duplicate batch jobs
- coordinating schema migrations
- protecting critical shared resources

Avoid if:

- idempotency can solve the problem
- partitioning work by key is enough
- optimistic concurrency is enough
- the lock would become a bottleneck

## How It Works

Basic lock flow:

1. Worker requests lock.
2. Lock service grants it if available.
3. Worker performs work.
4. Worker releases lock.
5. Lock expires if worker crashes.

Better flow with fencing:

1. Lock service grants lock with increasing fencing token.
2. Worker sends token to protected resource.
3. Resource rejects old tokens.

Fencing matters because a worker can pause, lose the lock, then continue later.

## Big Data / System Design Angle

Distributed locks are used around control-plane operations, not high-volume data paths.

Examples:

- one Airflow scheduler action
- one compaction job per table partition
- one leader per shard
- one metadata migration at a time

Safer alternatives:

- idempotent operations
- compare-and-set
- optimistic concurrency
- partition ownership
- consensus-backed leader election

## Failure Modes

- lock holder crashes
- lock expires while work continues
- network partition creates split brain
- client pauses due to GC
- lock service unavailable
- missing fencing allows stale worker writes

## Common Mistakes

- Mistake: Implementing locks with a simple database flag and no TTL.
- Better way: use transactional compare-and-set, TTL/lease, and recovery.

- Mistake: Using lock without fencing tokens.
- Better way: protect downstream resource from stale lock holders.

- Mistake: Locking too much.
- Better way: reduce critical section or partition the lock by resource.

## Interview Speak

"Distributed locks coordinate exclusive work across machines, but they are risky. I would prefer idempotency or partition ownership when possible. If I need a lock, I would use a proven consensus-backed system, leases with TTL, fencing tokens, monitoring, and small critical sections."

## Quick Recall

- One-liner: Distributed locks allow one actor across many machines, but need leases and fencing.
- Keywords: lease, fencing, split brain.
- Trap: Simple lock without fencing or expiry.
