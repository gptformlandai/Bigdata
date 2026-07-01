# Topic 018: Consistency Models

## Goal

Understand the different promises systems make about what reads can see after writes.

## Simple Explanation

Consistency models answer this question:

```text
After data is written, when will readers see it?
```

Some systems promise immediate latest reads. Others promise that updates will spread eventually.

## Core Idea

- Definition: A consistency model defines the visibility and ordering guarantees of reads and writes.
- Why it matters: It shapes user experience, correctness, latency, and availability.
- Related terms: strong consistency, eventual consistency, read-your-writes, causal consistency, linearizability.

## Common Models

| Model | Meaning | Example Fit |
|---|---|---|
| Strong consistency | reads return latest committed write | account balance |
| Linearizability | operations appear instant and globally ordered | distributed lock |
| Read-your-writes | user sees their own updates | profile update |
| Monotonic reads | once you see new data, you do not go backward | dashboards/session reads |
| Causal consistency | causally related events appear in order | comments and replies |
| Eventual consistency | replicas converge later | likes, feeds, counters |

## How It Is Used

Different product features can use different consistency models.

Example e-commerce system:

- payment ledger: strong consistency
- inventory reservation: strong or carefully coordinated
- product recommendations: eventual consistency
- product reviews count: eventual consistency
- user profile edit: read-your-writes

## Big Data / System Design Angle

Consistency affects:

- latency
- availability
- correctness
- user trust
- operational complexity

Stronger consistency often requires coordination:

```text
more coordination -> higher latency and lower availability under failure
```

Weaker consistency often requires reconciliation:

```text
more availability -> possible stale/conflicting data -> repair logic
```

## Example

User changes display name from `Aravind` to `Aravind M`.

Strong consistency:

```text
Every read immediately shows Aravind M.
```

Eventual consistency:

```text
Some services show Aravind for a short time.
Later all converge to Aravind M.
```

Read-your-writes:

```text
The user who changed it sees Aravind M immediately.
Other users may see old value briefly.
```

## Common Mistakes

- Mistake: Demanding strong consistency for every feature.
- Better way: Match consistency to business correctness.

- Mistake: Accepting eventual consistency without repair.
- Better way: Add idempotency, conflict resolution, reconciliation, and monitoring.

- Mistake: Not defining stale-read tolerance.
- Better way: State how stale data can be and who can see it.

## Interview Speak

"I would choose consistency based on the business invariant. Money, inventory, locks, and metadata usually need stronger guarantees. Feeds, likes, analytics, and recommendations can often be eventually consistent if we design reconciliation and tolerate stale reads."

## Quick Recall

- One-liner: Consistency models define when reads see writes.
- Keywords: strong, eventual, read-your-writes.
- Trap: Treating eventual consistency as "no correctness needed."
