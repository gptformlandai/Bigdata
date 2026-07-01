# Topic 059: Eventual Consistency

## Goal

Understand eventual consistency as a practical consistency model for scalable distributed systems.

## Simple Explanation

Eventual consistency means replicas may disagree briefly, but if no new updates happen, they eventually converge to the same value.

Example:

```text
Like count shows 100 in one region and 102 in another.
After replication catches up, both show 102.
```

## Core Idea

- Definition: Eventual consistency allows temporary stale or divergent reads while guaranteeing convergence eventually.
- Why it matters: It improves availability, latency, and scalability when immediate consistency is not required.
- Related terms: replication lag, conflict resolution, convergence, read repair, reconciliation.

## Where It Fits

Good fits:

- social likes
- feeds
- recommendations
- analytics dashboards
- search indexes
- product view counts
- cache updates

Poor fits:

- payment ledger
- account balance
- inventory finalization
- distributed locks
- authentication/authorization changes where stale access is dangerous

## How It Works

Typical flow:

1. Write accepted by one node/region.
2. Change is replicated asynchronously.
3. Some readers may see old data.
4. Replicas catch up.
5. Conflicts are resolved if needed.
6. System converges.

## Big Data / System Design Angle

Eventual consistency is common in data platforms because analytics often tolerates freshness delay.

Examples:

- dashboard updated every 5 minutes
- search index updated asynchronously
- warehouse table refreshed hourly
- ML feature store updated after stream processing delay

You must define:

- acceptable staleness
- conflict resolution
- reconciliation process
- user experience during lag
- monitoring for convergence

## Common Mistakes

- Mistake: Saying eventual consistency means "wrong is fine."
- Better way: define bounded staleness and reconciliation.

- Mistake: Not telling users data may be stale.
- Better way: show freshness timestamps for dashboards.

- Mistake: Ignoring conflicts.
- Better way: use versioning, vector clocks, last-write-wins only when safe, or business-specific merge logic.

## Interview Speak

"Eventual consistency allows replicas to be temporarily stale but converge later. I would use it for feeds, analytics, recommendations, and counters where availability and latency matter more than immediate correctness. I would define stale tolerance, conflict resolution, reconciliation, and lag monitoring."

## Quick Recall

- One-liner: Replicas may be stale now, but converge later.
- Keywords: stale, converge, reconciliation.
- Trap: Using eventual consistency for money or locks without safeguards.
