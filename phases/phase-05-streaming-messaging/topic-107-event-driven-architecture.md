# Topic 107: Event-Driven Architecture

## 1. Goal

Understand event-driven architecture as a way to build systems that react to things happening in real time.

## 2. Baby Intuition

Imagine a doorbell.

You do not keep asking every second, "Is someone at the door?"

Instead, when someone presses the bell, an event happens, and you react.

Event-driven architecture is the same idea for software:

```text
something happened -> publish an event -> interested systems react
```

## 3. What It Is

- Simple definition: Event-driven architecture is a design where systems communicate by producing and consuming events.
- Technical definition: Event-driven architecture decouples services through asynchronous event messages that represent facts about state changes or actions.
- Category: Distributed systems and data architecture pattern.
- Related terms: event, producer, consumer, broker, topic, stream, asynchronous, pub/sub.

## 4. Why It Exists

Without events, systems often call each other directly.

Direct calls create problems:

- services become tightly coupled
- one slow service slows another
- failures cascade
- new consumers require changing producers
- real-time analytics is harder
- historical replay is impossible unless logs are stored

Events solve this by letting producers say:

```text
This happened.
```

Consumers decide what to do.

## 5. Where It Fits In A Data Platform

```text
Applications / DB changes / Devices
  -> Event broker / stream platform
  -> Stream processors / data lake / dashboards / ML features
```

Examples of events:

- `OrderCreated`
- `PaymentAuthorized`
- `UserClickedProduct`
- `DriverLocationUpdated`
- `ClaimSubmitted`
- `SensorReadingCaptured`

## 6. How It Works Step By Step

Flow:

1. Something happens in a source system.
2. Producer creates an event.
3. Event is published to a broker or stream.
4. Broker stores/routes the event.
5. Consumers read the event.
6. Consumers update their own systems.
7. Failures are handled with retries, offsets, DLQs, or replay.

Example:

```text
User places order
  -> Order service emits OrderCreated
  -> Inventory service reserves item
  -> Email service sends confirmation
  -> Analytics pipeline updates dashboard
```

## 7. How To Use It Practically

Typical event shape:

```json
{
  "event_id": "evt_1001",
  "event_type": "OrderCreated",
  "order_id": "o123",
  "customer_id": "c9",
  "created_at": "2026-07-01T10:00:00Z"
}
```

Practical rules:

- include unique event id
- include event time
- define schema
- make consumers idempotent
- plan for retries and duplicates
- do not put unnecessary PII in events

## 8. Real-World Scenario

- Product/system: E-commerce order platform.
- Problem: Many systems need to react when an order is created.
- How events help: Order service emits one event; inventory, email, analytics, and fraud consumers react independently.
- What would go wrong without it: Order service would need direct calls to every downstream system.

## 9. System Design Angle

Use event-driven architecture when:

- multiple systems need the same fact
- asynchronous processing is acceptable
- replay/history is valuable
- producers and consumers should be decoupled
- real-time analytics is needed

Avoid or be careful when:

- strict immediate consistency is required
- workflow needs strong transaction across systems
- teams cannot handle eventual consistency

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| decoupled services | eventual consistency |
| scalable fan-out | harder debugging |
| real-time processing | duplicate/out-of-order events |
| replayable history | schema governance needed |

## 11. Failure Modes

- Failure: Consumer fails after processing but before committing.
- Symptom: event may be processed again.
- Recovery: retry and idempotent handling.
- Prevention: idempotency keys and careful offset commits.

- Failure: Bad event schema.
- Symptom: consumers fail parsing.
- Recovery: DLQ or schema rollback.
- Prevention: schema registry and compatibility rules.

- Failure: Event storm.
- Symptom: lag/backpressure.
- Recovery: scale consumers or throttle producers.
- Prevention: capacity planning.

## 12. Common Mistakes

- Mistake: Treating events like commands.
- Why it is wrong: an event says something happened; a command asks something to happen.
- Better approach: name facts in past tense like `OrderCreated`.

- Mistake: Ignoring duplicates.
- Why it is wrong: retries can produce or deliver duplicates.
- Better approach: design idempotent consumers.

## 13. Mini Example

Event naming:

```text
Good: PaymentCaptured
Risky: CapturePayment
```

The first is a fact. The second is a command.

## 14. Interview Questions

1. What is event-driven architecture?
2. Why does it decouple systems?
3. What are producers and consumers?
4. What are common failure modes?
5. How do you handle duplicate events?

## 15. Interview Speak

"Event-driven architecture lets systems communicate by publishing facts as events. Producers do not need to know every consumer, and consumers can independently react, replay, or process asynchronously. The trade-offs are eventual consistency, duplicate/out-of-order events, schema governance, and harder debugging."

## 16. Quick Recall

- One-line summary: Systems publish facts and other systems react.
- Three keywords: event, producer, consumer.
- One trap: Forgetting duplicates and eventual consistency.
- One memory trick: Doorbell, not constant polling.
