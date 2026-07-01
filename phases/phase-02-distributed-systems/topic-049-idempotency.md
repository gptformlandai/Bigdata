# Topic 049: Idempotency

## Goal

Understand idempotency as a core safety property for retries, event processing, APIs, and distributed writes.

## Simple Explanation

An operation is idempotent if doing it multiple times has the same effect as doing it once.

Example:

```text
Set account status to ACTIVE
```

Doing this once or five times leaves the status as ACTIVE.

Non-idempotent example:

```text
Add $10 to balance
```

Doing this five times adds $50.

## Core Idea

- Definition: Idempotency means repeated execution produces the same final state.
- Why it matters: Distributed systems retry after failures, and retries can create duplicates.
- Related terms: idempotency key, deduplication, exactly-once, retry, event id, upsert.

## How It Is Used

Used in:

- payment APIs
- order creation
- Kafka consumers
- data pipeline writes
- REST APIs
- job retries
- CDC processing

Common techniques:

- idempotency keys
- unique event ids
- upserts instead of inserts
- deterministic output paths
- transaction logs
- deduplication tables
- compare-and-set

## Example

Bad retry behavior:

```text
POST /charge $100
timeout
client retries
customer charged twice
```

Idempotent behavior:

```text
POST /charge $100 with idempotency_key=abc123
timeout
client retries with same key
server returns original result
customer charged once
```

## Big Data / System Design Angle

Idempotency is essential because many data systems provide at-least-once delivery.

That means:

```text
events may arrive more than once
```

So consumers must safely handle duplicates.

Examples:

- Use event id to deduplicate clicks.
- Use merge/upsert for CDC records.
- Write output partition atomically.
- Track processed offsets only after successful commit.

## Common Mistakes

- Mistake: Relying on "exactly once" marketing.
- Better way: Still design idempotent sinks and consumers.

- Mistake: Generating a new idempotency key on retry.
- Better way: Reuse the same key for the same logical operation.

- Mistake: Deduplicating only in memory.
- Better way: Use durable deduplication for important workflows.

## Interview Speak

"Idempotency makes retries safe. If an operation may be attempted multiple times, I use an idempotency key, event id, upsert, or deterministic write so repeated attempts do not double-charge, double-count, or duplicate data."

## Quick Recall

- One-liner: Idempotency makes repeat attempts safe.
- Keywords: retry, dedupe, idempotency key.
- Trap: Calling an API idempotent when retries create new side effects.
