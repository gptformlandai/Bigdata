# Topic 044: Leader / Follower Architecture

## Goal

Understand how leader/follower replication organizes writes, reads, and failover.

## Simple Explanation

One node is the leader. It accepts writes.

Followers copy the leader's data and can often serve reads.

## Core Idea

- Definition: Leader/follower architecture uses one primary node for writes and one or more replicas for replication and reads.
- Why it matters: It simplifies write ordering and enables read scaling and failover.
- Related terms: primary, replica, follower, failover, replication lag, split brain.

## How It Works

Write path:

1. Client sends write to leader.
2. Leader commits the write.
3. Leader replicates the write to followers.
4. Followers apply the write.

Read path options:

- read from leader for freshest data
- read from followers for scale and lower load
- use read-your-writes routing for user experience

Failover:

1. Leader becomes unhealthy.
2. System detects failure.
3. A follower is promoted.
4. Clients route to new leader.

## Big Data / System Design Angle

Leader/follower appears in:

- relational databases
- Kafka partition leaders and followers
- metadata systems
- search clusters
- replicated key-value stores

Trade-offs:

| Benefit | Cost |
|---|---|
| simpler write ordering | leader bottleneck |
| easier replication model | failover complexity |
| read scaling via followers | stale follower reads |
| operational clarity | split-brain risk if election is wrong |

## Common Mistakes

- Mistake: Sending writes to followers.
- Better way: Route writes to leader unless system supports multi-leader writes.

- Mistake: Ignoring replication lag.
- Better way: monitor lag and use leader reads for correctness-sensitive flows.

- Mistake: Allowing two leaders.
- Better way: use reliable leader election and fencing.

## Interview Speak

"Leader/follower architecture sends writes to a leader, which replicates to followers. This simplifies ordering and enables read scaling, but introduces leader bottlenecks, replication lag, and failover concerns. For strong reads I would use the leader or quorum; for scalable reads I may use followers with lag monitoring."

## Quick Recall

- One-liner: Leader writes; followers copy.
- Keywords: primary, replica, lag.
- Trap: Ignoring split brain during failover.
