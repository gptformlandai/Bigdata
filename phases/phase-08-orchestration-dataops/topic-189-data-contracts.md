# Topic 189: Data Contracts

## 1. Goal

Understand data contracts as agreements between data producers and consumers.

## 2. Baby Intuition

A data contract is like an API contract for data.

If a producer promises `order_id` is always present and `amount` is numeric, consumers can build safely.

## 3. What It Is

- Simple definition: A data contract defines what data producers promise to deliver.
- Technical definition: A data contract is a documented and enforceable agreement about schema, semantics, quality, freshness, ownership, and change management for a dataset or event.
- Category: Data governance and reliability.
- Related terms: schema, SLA, owner, compatibility, producer, consumer, data product.

## 4. Why It Exists

Downstream pipelines break when upstream changes happen silently:

- column renamed
- type changed
- nullable field becomes null
- enum value changes
- metric meaning changes
- data arrives late

Data contracts make producers accountable and consumers safer.

## 5. Where It Fits In A Data Platform

```text
producer service/team
  -> data contract
  -> event/table/schema validation
  -> consumers/pipelines
```

Contracts are useful for Kafka events, database CDC, warehouse tables, and data products.

## 6. How It Works Step By Step

1. Identify data producer and consumers.
2. Define schema and field meanings.
3. Define quality and freshness expectations.
4. Define compatibility/change rules.
5. Validate data against contract.
6. Alert/block when contract is violated.
7. Version contract when changes are needed.

## 7. How To Use It Practically

Contract contents:

| Area | Example |
|---|---|
| schema | order_id string, amount decimal |
| semantics | amount excludes tax |
| quality | order_id not null |
| freshness | delivered within 15 minutes |
| owner | checkout team |
| compatibility | cannot remove fields without notice |
| PII | customer_email is sensitive |

## 8. Real-World Scenario

- Product/system: Order events.
- Problem: Checkout service changes `amount` from cents to dollars without telling analytics.
- How contract helps: semantic/version change must be reviewed and validated.
- What would go wrong without it: revenue numbers become 100x wrong.

## 9. System Design Angle

Mention data contracts when:

- many downstream consumers depend on upstream data
- schema changes break pipelines
- producer ownership matters
- event-driven/lakehouse pipelines need reliability
- data product thinking is required

Key phrase:

```text
Data contracts move quality left, closer to producers.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| fewer breaking changes | requires producer buy-in |
| clear ownership | contract maintenance |
| better consumer trust | may slow rapid schema changes |
| enforceable quality | needs validation tooling |

## 11. Failure Modes

- Failure: Contract not enforced.
- Symptom: documented promise but bad data still flows.
- Recovery: add validation gates.
- Prevention: automate checks.

- Failure: No owner.
- Symptom: contract violations unresolved.
- Recovery: assign producer owner.
- Prevention: ownership required.

- Failure: Overly strict contract.
- Symptom: harmless changes blocked.
- Recovery: compatibility rules.
- Prevention: versioning strategy.

## 12. Common Mistakes

- Mistake: Treating contracts as documentation only.
- Why it is wrong: docs can drift from reality.
- Better approach: enforce contracts in CI/runtime.

- Mistake: Defining schema but not meaning.
- Why it is wrong: field type can stay same while business meaning changes.
- Better approach: include semantics and examples.

## 13. Mini Example

```text
Dataset: order_created
owner: checkout-platform
order_id: required string
amount_cents: required integer >= 0
currency: accepted values USD, INR, EUR
freshness: available within 5 minutes
```

## 14. Interview Questions

1. What is a data contract?
2. Why are data contracts useful?
3. What should a contract include?
4. How do contracts prevent breaking changes?
5. Contract vs schema?

## 15. Interview Speak

"A data contract is an agreement between producers and consumers about schema, semantics, quality, freshness, ownership, and change management. I would enforce it through schema validation, CI checks, runtime checks, alerts, and versioning so upstream changes do not silently break downstream data products."

## 16. Quick Recall

- One-line summary: Data contracts make producer promises explicit and enforceable.
- Three keywords: schema, semantics, owner.
- One trap: Contract as static docs only.
- One memory trick: API contract for data.
