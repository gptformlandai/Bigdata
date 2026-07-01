# Topic 056: Clock Skew

## Goal

Understand why clocks differ across machines and how that affects distributed systems.

## Simple Explanation

Clock skew means different machines disagree about the current time.

In distributed systems, this matters because events happen on different machines, and timestamps may lie or arrive out of order.

## Core Idea

- Definition: Clock skew is the difference between clocks on different machines.
- Why it matters: Ordering, expiration, logging, leases, and event-time processing often depend on time.
- Related terms: NTP, logical clock, vector clock, event time, processing time, watermark.

## Why It Happens

Clocks differ because:

- hardware clocks drift
- NTP sync is not instant
- virtual machines pause/resume
- network delays vary
- regions have different latency

## Where It Hurts

Clock skew can break:

- event ordering
- TTL expiration
- distributed locks and leases
- log correlation
- audit trails
- stream processing windows
- conflict resolution based on "latest timestamp wins"

## Big Data / System Design Angle

Streaming systems separate:

- event time: when event actually happened
- processing time: when system processed it

Example:

```text
event happened at 10:00
event arrived at 10:07
```

Late arrival can happen due to mobile clients, network delay, batching, or outages.

## Mitigations

- synchronize clocks with NTP
- use server-side timestamps where possible
- use monotonic clocks for measuring durations
- avoid relying only on wall-clock time for correctness
- use logical clocks or version numbers
- use watermarks and allowed lateness in streaming
- design leases with clock-skew safety margins

## Common Mistakes

- Mistake: Ordering distributed events only by client timestamp.
- Better way: combine event time, ingestion time, sequence ids, and watermarks.

- Mistake: Using wall-clock time for measuring elapsed duration.
- Better way: use monotonic clocks.

- Mistake: Assuming NTP removes all skew.
- Better way: assume bounded but nonzero skew.

## Interview Speak

"Clock skew means machines disagree on time. I would avoid relying on wall-clock timestamps for critical ordering or locks. For analytics and streaming, I would distinguish event time from processing time and use watermarks, allowed lateness, and server-side timestamps where appropriate."

## Quick Recall

- One-liner: Distributed machines do not share perfect time.
- Keywords: event time, processing time, watermark.
- Trap: Ordering everything by client timestamp.
