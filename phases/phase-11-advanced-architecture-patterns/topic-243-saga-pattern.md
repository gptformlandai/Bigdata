# Topic 243: Saga Pattern

## 1. Goal

Understand Saga pattern as a way to manage multi-step distributed business transactions.

## 2. Baby Intuition

A saga is like a travel plan with refunds.

If booking the flight succeeds but hotel booking fails, the system runs a compensating action to cancel or refund the flight.

## 3. What It Is

- Simple definition: Saga pattern breaks a distributed transaction into steps with compensating actions.
- Technical definition: Saga pattern coordinates a sequence of local transactions across services, where each step publishes events or commands and failures trigger compensating transactions.
- Category: Distributed transaction / consistency pattern.
- Related terms: choreography, orchestration, compensation, eventual consistency, microservices, outbox.

## 4. Why It Exists

Distributed systems often need multiple services to update state:

- order service
- payment service
- inventory service
- shipping service

Using one global database transaction across all services is usually impractical.

Saga pattern manages the workflow with local transactions and compensation.

## 5. Where It Fits In A Data Platform

Sagas are mostly application/microservice patterns, but they affect data platforms because they produce events and state changes that analytics must interpret.

```text
OrderCreated -> PaymentReserved -> InventoryReserved -> OrderConfirmed
```

Analytics should understand intermediate states and compensations.

## 6. How It Works Step By Step

Orchestrated saga:

1. Saga orchestrator starts workflow.
2. Service A runs local transaction.
3. Service B runs local transaction.
4. Service C fails.
5. Orchestrator sends compensating commands to B and A.
6. Final state becomes cancelled/failed.

Choreographed saga:

1. Service emits event.
2. Other services react.
3. Failure events trigger compensating actions.

## 7. How To Use It Practically

Saga needs:

- clear business states
- idempotent commands/events
- compensation logic
- timeouts
- monitoring
- audit trail
- outbox pattern for reliable events

Common state machine:

```text
created -> payment_reserved -> inventory_reserved -> confirmed
created -> payment_failed -> cancelled
```

## 8. Real-World Scenario

- Product/system: E-commerce order checkout.
- Problem: Order creation, payment, inventory, and shipping happen in different services.
- How Saga helps: each service commits locally; failures trigger compensating actions like payment refund or inventory release.
- What would go wrong without it: partial order states become inconsistent with no recovery plan.

## 9. System Design Angle

Use Saga when:

- one business transaction spans multiple services
- strong distributed transaction is unavailable/unwanted
- compensation is possible
- eventual consistency is acceptable

Avoid when:

- one local transaction is enough
- compensation is impossible or legally risky
- strict immediate consistency is required

## 10. Trade-offs

| Pros | Cons |
|---|---|
| avoids distributed locks/2PC | eventual consistency |
| works across services | complex failure states |
| explicit recovery | compensation logic is hard |
| good audit trail | users may see pending states |

## 11. Failure Modes

- Failure: Compensation fails.
- Symptom: system stuck in inconsistent state.
- Recovery: retry/manual intervention.
- Prevention: idempotent compensations and alerts.

- Failure: Duplicate events.
- Symptom: step runs twice.
- Recovery: dedupe/idempotency.
- Prevention: event IDs and state checks.

- Failure: Missing timeout.
- Symptom: saga waits forever.
- Recovery: timeout and compensation.
- Prevention: deadline policy.

## 12. Common Mistakes

- Mistake: Treating Saga as ACID transaction.
- Why it is wrong: saga gives eventual consistency with compensations.
- Better approach: model intermediate states clearly.

- Mistake: No business-approved compensation.
- Why it is wrong: technical rollback may not match business/legal reality.
- Better approach: define compensation with product/domain teams.

## 13. Mini Example

```text
reserve_payment succeeds
reserve_inventory fails
compensate:
  release_payment
  mark_order_cancelled
```

## 14. Interview Questions

1. What is Saga pattern?
2. Choreography vs orchestration?
3. What is compensation?
4. Why is Saga eventually consistent?
5. How do events and idempotency fit?

## 15. Interview Speak

"Saga pattern coordinates multi-service business transactions using local commits and compensating actions. I would use it when distributed ACID transactions are not practical, with explicit states, idempotent commands, timeouts, monitoring, and business-approved compensation logic."

## 16. Quick Recall

- One-line summary: Saga is multi-step transaction plus compensation.
- Three keywords: local transaction, compensation, eventual consistency.
- One trap: Assuming it gives instant ACID consistency.
- One memory trick: If hotel fails, cancel the flight.
