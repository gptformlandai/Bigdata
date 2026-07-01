# Topic 057: Exactly-Once vs At-Least-Once vs At-Most-Once

## Goal

Understand delivery semantics and what guarantees a system provides when messages or events are processed.

## Simple Explanation

Delivery semantics answer:

```text
How many times might this message be processed?
```

Three common answers:

- at-most-once: maybe once, maybe lost
- at-least-once: one or more times
- exactly-once: appears once in the final result under specific conditions

## Core Idea

- Definition: Delivery semantics describe how message delivery and processing behave under failures and retries.
- Why it matters: Data systems must avoid unacceptable data loss or duplication.
- Related terms: offset, commit, retry, idempotency, deduplication, transaction, sink.

## Comparison

| Semantics | Meaning | Risk | Common Use |
|---|---|---|---|
| At-most-once | process zero or one time | data loss | low-value telemetry |
| At-least-once | process one or more times | duplicates | most reliable pipelines |
| Exactly-once | final effect appears once | complexity | financial-ish aggregates, critical streams |

## At-Most-Once

Flow:

1. Mark message as processed.
2. Try processing.
3. If processing fails, message is lost.

Low latency, but can lose data.

## At-Least-Once

Flow:

1. Process message.
2. Commit offset/result after success.
3. If failure happens before commit, message is retried.

Reliable, but duplicates can occur.

## Exactly-Once

Usually means exactly-once effect, not magic.

Requires coordination between:

- source
- processor
- state
- sink
- transaction/commit protocol

Even then, external side effects may still need idempotency.

## Big Data / System Design Angle

Most systems should assume at-least-once and design idempotent consumers.

Examples:

- Kafka consumer may reprocess messages after crash.
- Spark job rerun may write duplicate output if not careful.
- API retry may submit same operation twice.

## Common Mistakes

- Mistake: Thinking exactly-once means no message is ever retried.
- Better way: Exactly-once usually means final committed result is not duplicated.

- Mistake: Ignoring sink behavior.
- Better way: The sink must support idempotent or transactional writes.

- Mistake: Using at-most-once for important data.
- Better way: Use at-least-once plus dedupe/idempotency.

## Interview Speak

"At-most-once can lose messages, at-least-once can duplicate messages, and exactly-once usually means exactly-once final effect with transactional coordination. In practice I often design for at-least-once delivery with idempotent writes and deduplication."

## Quick Recall

- One-liner: Delivery semantics define loss and duplicate behavior.
- Keywords: loss, duplicate, idempotency.
- Trap: Believing exactly-once removes the need to reason about side effects.
