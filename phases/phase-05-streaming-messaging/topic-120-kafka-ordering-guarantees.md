# Topic 120: Kafka Ordering Guarantees

## 1. Goal

Understand what ordering Kafka guarantees and how to design partition keys correctly.

## 2. Baby Intuition

Kafka has many lanes.

Cars in the same lane stay ordered. Cars in different lanes do not have one global order.

## 3. What It Is

- Simple definition: Kafka preserves order within a partition.
- Technical definition: Kafka guarantees records are stored and consumed in offset order within a single partition, but not across partitions.
- Category: Event ordering guarantee.
- Related terms: partition, key, offset, producer order, consumer group.

## 4. Why It Exists

Global order across a distributed system is expensive.

Kafka chooses scalable ordering:

```text
order within partition
parallelism across partitions
```

## 5. Where It Fits In A Data Platform

Ordering matters in streams like:

- account balance changes
- order lifecycle events
- CDC row changes
- user session events
- inventory updates

## 6. How It Works Step By Step

If producer sends with same key:

```text
key=order-1 -> partition 2
```

All records for `order-1` go to partition 2 if partition count/keying is stable.

Kafka appends:

```text
offset 10: OrderCreated
offset 11: PaymentCaptured
offset 12: OrderShipped
```

Consumer reads in offset order.

## 7. How To Use It Practically

Choose key based on ordering need:

```text
Need per user order -> key=user_id
Need per order order -> key=order_id
Need per account order -> key=account_id
```

Producer config for strong ordering with retries:

```properties
enable.idempotence=true
max.in.flight.requests.per.connection=5
```

Modern Kafka idempotence helps preserve ordering with retries.

## 8. Real-World Scenario

- Product/system: Order lifecycle stream.
- Problem: Consumers must see `OrderCreated` before `OrderShipped` for the same order.
- How ordering helps: Use `order_id` as key so events for same order land in one partition.
- What would go wrong without it: downstream state machine may see shipped before created.

## 9. System Design Angle

Ordering trade-off:

```text
more ordering requirement -> less parallelism
```

If all events must be globally ordered, one partition may be required, but throughput suffers.

Usually better:

```text
per-entity ordering
```

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| per-key order | hot key risk |
| scalable partitions | no global order |
| deterministic state updates | key choice matters |

## 11. Failure Modes

- Failure: wrong partition key.
- Symptom: related events land in different partitions and reorder.
- Recovery: redesign topic/key and migrate.
- Prevention: define ordering requirement first.

- Failure: hot ordered key.
- Symptom: one partition overloaded.
- Recovery: split entity if business allows.
- Prevention: key distribution analysis.

## 12. Common Mistakes

- Mistake: Expecting order across partitions.
- Why it is wrong: Kafka only orders within partitions.
- Better approach: key related events together.

- Mistake: Random keys for ordered workflows.
- Why it is wrong: related events scatter.
- Better approach: use entity id as key.

## 13. Mini Example

```text
key=user_1:
offset 0 login
offset 1 click
offset 2 purchase
```

Same user events stay ordered if keyed to same partition.

## 14. Interview Questions

1. What ordering does Kafka guarantee?
2. How does partition key affect ordering?
3. Does Kafka guarantee global order?
4. How do retries affect ordering?
5. What if one key is very hot?

## 15. Interview Speak

"Kafka guarantees ordering only within a partition. To preserve order for an entity, I key events by that entity id so all related events go to the same partition. Global ordering would require sacrificing parallelism, so most designs use per-key ordering."

## 16. Quick Recall

- One-line summary: Kafka order is per partition, not global.
- Three keywords: key, partition, offset.
- One trap: Random keys for ordered events.
- One memory trick: Same lane, same order.
