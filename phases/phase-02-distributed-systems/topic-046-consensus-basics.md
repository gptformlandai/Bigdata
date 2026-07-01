# Topic 046: Consensus Basics

## Goal

Understand why consensus exists and what problem it solves in distributed systems.

## Simple Explanation

Consensus is how multiple machines agree on one decision even when some machines fail.

Example decisions:

- Who is the leader?
- Was this write committed?
- What is the next value in the log?

## Core Idea

- Definition: Consensus is a protocol that lets distributed nodes agree on a value or sequence of values despite failures.
- Why it matters: Critical cluster decisions must be correct, not just fast.
- Related terms: leader election, replicated log, quorum, Raft, Paxos, split brain.

## What Consensus Solves

Consensus prevents dangerous disagreement.

Without consensus:

- two leaders may accept writes
- metadata may diverge
- locks may be granted twice
- committed state may be unclear

With consensus:

- nodes agree on committed operations
- failover is controlled
- metadata changes are ordered

## Where It Is Used

Consensus appears in:

- leader election
- distributed metadata stores
- configuration management
- cluster membership
- distributed locks
- replicated logs
- systems like etcd, ZooKeeper, Consul

## Big Data / System Design Angle

Consensus is usually not used for every data record in high-throughput Big Data paths because it is expensive.

Common pattern:

```text
Use consensus for control plane.
Use partitioned/replicated data paths for high-throughput data.
```

Examples:

- Kafka uses consensus-like mechanisms for metadata/control depending on mode.
- HDFS-like systems rely on metadata coordination.
- Kubernetes uses etcd for cluster state.

## Trade-offs

| Gain | Cost |
|---|---|
| correct agreement | coordination overhead |
| safe leader election | higher latency |
| avoids split brain | quorum availability dependency |
| ordered metadata changes | operational complexity |

## Common Mistakes

- Mistake: Using consensus for every event in a high-throughput analytics stream.
- Better way: Use consensus for metadata/control, not every data message unless required.

- Mistake: Ignoring quorum availability.
- Better way: If a majority is unavailable, consensus cannot safely progress.

- Mistake: Saying consensus is just voting.
- Better way: It is a carefully designed protocol for agreement under failure.

## Interview Speak

"Consensus lets distributed nodes agree on critical decisions like leader election or committed log entries. It prevents split brain and inconsistent metadata, but it adds latency and requires quorum. I would use it for control-plane correctness, not blindly for every high-throughput data operation."

## Quick Recall

- One-liner: Consensus is safe agreement under failure.
- Keywords: leader election, quorum, log.
- Trap: Treating consensus as cheap.
