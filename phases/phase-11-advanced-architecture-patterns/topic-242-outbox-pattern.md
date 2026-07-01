# Topic 242: Outbox Pattern

## 1. Goal

Understand the Outbox pattern for reliably publishing events from a database-backed service.

## 2. Baby Intuition

The Outbox pattern is like writing a receipt in the same notebook as the sale.

If the sale is saved, the event to announce the sale is saved too.

## 3. What It Is

- Simple definition: Outbox pattern stores events in the same database transaction as business data.
- Technical definition: The Outbox pattern writes domain changes and corresponding event records to an outbox table in one local transaction, then a relay publishes those events to a broker.
- Category: Reliability pattern for event-driven systems.
- Related terms: transactional outbox, event relay, CDC, Debezium, Kafka, exactly-once effect, idempotency.

## 4. Why It Exists

A service often needs to:

1. update its database
2. publish an event

Naive problem:

```text
database update succeeds
event publish fails
```

or:

```text
event publish succeeds
database update fails
```

Outbox pattern keeps the database change and event record atomic.

## 5. Where It Fits In A Data Platform

```text
service transaction
  -> business table update
  -> outbox table insert
  -> relay/CDC publishes outbox event
  -> Kafka/event bus
  -> data pipelines/services
```

## 6. How It Works Step By Step

1. Service receives command.
2. Service starts database transaction.
3. Service writes business row changes.
4. Service writes event record to outbox table.
5. Transaction commits.
6. Relay reads unpublished outbox records.
7. Relay publishes events to broker.
8. Relay marks event as published or relies on idempotency.
9. Consumers process events idempotently.

## 7. How To Use It Practically

Outbox table fields:

| Field | Meaning |
|---|---|
| event_id | unique event identifier |
| aggregate_id | business entity ID |
| event_type | OrderCreated, PaymentCaptured |
| payload | event body |
| created_at | event creation time |
| published_at/status | relay progress if used |

Relay options:

- polling publisher
- Debezium CDC on outbox table
- database trigger-based relay

## 8. Real-World Scenario

- Product/system: Order service.
- Problem: When an order is created, analytics, inventory, and email systems need an event.
- How Outbox helps: order row and OrderCreated event are committed together; relay later publishes event reliably.
- What would go wrong without it: order exists but downstream systems never hear about it.

## 9. System Design Angle

Use Outbox when:

- service owns database
- reliable event publishing is needed
- distributed transaction with broker is undesirable
- event-driven downstream systems depend on changes

Be careful with:

- duplicate event publishes
- outbox cleanup
- relay lag
- idempotent consumers
- event schema evolution

## 10. Trade-offs

| Pros | Cons |
|---|---|
| atomic DB change + event record | extra outbox table/relay |
| avoids distributed transaction | duplicate publish possible |
| works with CDC | relay lag must be monitored |
| improves reliability | cleanup/retention needed |

## 11. Failure Modes

- Failure: Relay down.
- Symptom: outbox grows, downstream stale.
- Recovery: restart relay.
- Prevention: lag/backlog alerts.

- Failure: Event published twice.
- Symptom: consumer duplicate effects.
- Recovery: dedupe by event_id.
- Prevention: idempotent consumers.

- Failure: Outbox never cleaned.
- Symptom: table grows forever.
- Recovery: archive/delete old published events.
- Prevention: retention policy.

## 12. Common Mistakes

- Mistake: Publishing event before database commit.
- Why it is wrong: consumers may see event for data that never committed.
- Better approach: write outbox record in the same transaction.

- Mistake: Assuming Outbox gives exactly-once consumers.
- Why it is wrong: relay may publish duplicates.
- Better approach: include event_id and make consumers idempotent.

## 13. Mini Example

```text
Transaction:
insert into orders(id=10, status='created')
insert into outbox(event_id='e1', type='OrderCreated', aggregate_id=10)
commit

Relay:
publish e1 to Kafka
```

## 14. Interview Questions

1. What is the Outbox pattern?
2. What problem does it solve?
3. How does Debezium help Outbox?
4. Why do consumers still need idempotency?
5. How do you monitor outbox relay lag?

## 15. Interview Speak

"The Outbox pattern writes business data and the event record in the same local database transaction. A relay or CDC process publishes the outbox event to Kafka or another broker. This avoids the database-update/event-publish dual-write problem, but consumers must still handle duplicates."

## 16. Quick Recall

- One-line summary: Outbox atomically stores business change and event-to-publish.
- Three keywords: transaction, outbox table, relay.
- One trap: Forgetting duplicate publishes.
- One memory trick: Receipt saved with the sale.
