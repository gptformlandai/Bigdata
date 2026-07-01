# Topic 244: Event Sourcing

## 1. Goal

Understand Event Sourcing as storing state changes as events instead of only current state.

## 2. Baby Intuition

Instead of storing only your current bank balance, event sourcing stores every deposit and withdrawal.

The current balance is rebuilt from the event history.

## 3. What It Is

- Simple definition: Event sourcing stores every state change as an event.
- Technical definition: Event sourcing persists an append-only sequence of domain events as the source of truth and derives current state by replaying those events.
- Category: Application/data architecture pattern.
- Related terms: event log, aggregate, projection, replay, CQRS, audit, append-only.

## 4. Why It Exists

Current-state tables answer:

```text
what is the value now?
```

Event sourcing also answers:

```text
how did it become this value?
```

Useful for:

- audit history
- replay/rebuild
- debugging
- temporal queries
- derived projections
- event-driven systems

## 5. Where It Fits In A Data Platform

```text
domain events
  -> append-only event store
  -> projections/read models
  -> analytics, search, features, dashboards
```

Event sourcing produces rich streams for downstream data systems.

## 6. How It Works Step By Step

1. User command occurs.
2. Application validates command.
3. Application appends domain event to event store.
4. Current state is derived by applying events.
5. Projections update read models.
6. New projections can be built by replaying events.

Example:

```text
AccountCreated
MoneyDeposited
MoneyWithdrawn
```

## 7. How To Use It Practically

Important concepts:

| Concept | Meaning |
|---|---|
| event store | append-only source of truth |
| aggregate | business entity with event history |
| projection | derived read model |
| replay | rebuild state from events |
| event version | schema evolution for events |

Good practices:

- events should be immutable
- use meaningful domain events
- version event schemas
- make projections idempotent
- monitor replay and projection lag

## 8. Real-World Scenario

- Product/system: Payment ledger.
- Problem: Need full audit trail of balance changes.
- How event sourcing helps: every debit/credit is stored as event; balance projection is derived.
- What would go wrong with current-state only: difficult to audit how balance changed.

## 9. System Design Angle

Use event sourcing when:

- audit trail is core
- history/replay matters
- multiple read models are needed
- domain events are meaningful

Avoid when:

- simple CRUD is enough
- team cannot handle event schema evolution
- replay/projection complexity is unnecessary

## 10. Trade-offs

| Pros | Cons |
|---|---|
| complete history | more complex model |
| easy replay/projections | event schema evolution |
| strong auditability | eventual consistency in projections |
| enables temporal analysis | storage grows append-only |

## 11. Failure Modes

- Failure: Bad event schema design.
- Symptom: hard to evolve/replay.
- Recovery: version and migration logic.
- Prevention: event design review.

- Failure: Projection lag.
- Symptom: read model stale.
- Recovery: scale projection consumers.
- Prevention: lag monitoring.

- Failure: Event meaning changes.
- Symptom: old events replay incorrectly.
- Recovery: versioned handlers.
- Prevention: immutable event semantics.

## 12. Common Mistakes

- Mistake: Storing technical database changes instead of domain events.
- Why it is wrong: downstream users need business meaning.
- Better approach: emit events like OrderPlaced, not just row_updated.

- Mistake: Using event sourcing for every CRUD app.
- Why it is wrong: complexity may not be justified.
- Better approach: use it when history/replay/audit is central.

## 13. Mini Example

```text
Events:
OrderCreated(order_id=1)
PaymentCaptured(order_id=1)
OrderShipped(order_id=1)

Projection:
orders_current.status = shipped
```

## 14. Interview Questions

1. What is event sourcing?
2. Event store vs current-state table?
3. What is a projection?
4. Why is replay useful?
5. What are event schema evolution risks?

## 15. Interview Speak

"Event sourcing stores immutable domain events as the source of truth and derives current state through projections. It is powerful for audit, replay, and multiple read models, but adds complexity around event design, schema evolution, projection lag, and storage growth."

## 16. Quick Recall

- One-line summary: Event sourcing stores every state change as immutable events.
- Three keywords: event store, projection, replay.
- One trap: Changing old event meanings.
- One memory trick: Balance from deposits and withdrawals.
