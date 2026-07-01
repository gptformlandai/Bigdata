# Topic 058: Ordering Guarantees

## Goal

Understand when distributed systems preserve event order and when they do not.

## Simple Explanation

Ordering guarantees answer:

```text
Will events be processed in the same order they happened or were written?
```

In distributed systems, global ordering is expensive. Many systems only guarantee order within a partition, key, or single connection.

## Core Idea

- Definition: Ordering guarantees define the sequence in which operations or events are observed and processed.
- Why it matters: Some workflows require order; others can tolerate reordering.
- Related terms: partition order, total order, causal order, sequence number, offset.

## Common Ordering Types

| Type | Meaning | Example |
|---|---|---|
| No order | events may arrive any order | logs from many services |
| Per-key order | same key stays ordered | Kafka events by user_id |
| Partition order | order within partition | Kafka partition offsets |
| Causal order | cause appears before effect | comment before reply |
| Total order | everyone sees same global order | consensus log |

## Big Data / System Design Angle

Ordering matters for:

- bank transactions
- inventory changes
- CDC events
- user session events
- state machines
- stream aggregations
- fraud rules

But ordering costs:

- lower parallelism
- coordination overhead
- hot partitions
- higher latency

## Example

User events:

```text
1. add_to_cart
2. checkout
3. payment_success
```

If processed out of order:

```text
payment_success before checkout
```

Downstream logic may break.

Kafka pattern:

```text
Use user_id as key -> all events for same user go to same partition -> per-user order
```

## Common Mistakes

- Mistake: Assuming global order in Kafka.
- Better way: Kafka guarantees order within a partition, not across all partitions.

- Mistake: Choosing random partition keys for ordered workflows.
- Better way: key by entity that needs order.

- Mistake: Forcing total order unnecessarily.
- Better way: use per-key order when global order is not required.

## Interview Speak

"Ordering guarantees should match the business requirement. Global order is expensive and reduces parallelism, so I would prefer per-key or partition-level ordering when possible. For Kafka, ordering is guaranteed within a partition, so the partition key must represent the entity whose events must stay ordered."

## Quick Recall

- One-liner: Order is usually local, not global.
- Keywords: partition, key, sequence.
- Trap: Assuming order across partitions.
