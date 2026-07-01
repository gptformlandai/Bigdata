# Topic 206: GCP Pub/Sub

## 1. Goal

Understand Pub/Sub as GCP's managed messaging and event ingestion service.

## 2. Baby Intuition

Pub/Sub is like a cloud mailbox for events.

Publishers send messages to a topic; subscribers receive and process them.

## 3. What It Is

- Simple definition: Pub/Sub is GCP's managed publish-subscribe messaging service.
- Technical definition: Google Cloud Pub/Sub provides asynchronous messaging through topics and subscriptions for event-driven systems, streaming ingestion, and service decoupling.
- Category: Managed messaging / event streaming.
- Related terms: topic, subscription, publisher, subscriber, ack, push, pull, ordering key, dead-letter topic.

## 4. Why It Exists

Systems need decoupling:

- applications emit events
- analytics consumes events
- alerts consume events
- storage sink consumes events
- ML feature pipeline consumes events

Pub/Sub lets producers publish once and consumers process independently.

## 5. Where It Fits In A Data Platform

```text
apps/services/devices
  -> Pub/Sub topic
  -> Dataflow subscribers / Cloud Functions / services
  -> BigQuery / Cloud Storage / alerts
```

## 6. How It Works Step By Step

1. Publisher sends message to topic.
2. Pub/Sub stores and delivers message to subscriptions.
3. Subscriber pulls or receives pushed message.
4. Subscriber processes message.
5. Subscriber acknowledges success.
6. Unacknowledged messages can be redelivered.
7. DLQ/dead-letter topic can handle repeated failures.

## 7. How To Use It Practically

Important concepts:

| Concept | Meaning |
|---|---|
| topic | named stream of published messages |
| subscription | consumer view of topic |
| ack | subscriber confirms message processed |
| push | Pub/Sub calls subscriber endpoint |
| pull | subscriber asks for messages |
| ordering key | preserve order for related messages where configured |

Good practices:

- design idempotent subscribers
- use dead-letter topics
- monitor undelivered messages/latency
- keep message payloads reasonable
- use schemas/contracts for important events

## 8. Real-World Scenario

- Product/system: Order event platform.
- Problem: Order service must notify analytics, email, fraud, and inventory independently.
- How Pub/Sub helps: publish order events to topic; each consumer uses its own subscription.
- What would go wrong without it: order service becomes tightly coupled to every consumer.

## 9. System Design Angle

Use Pub/Sub when:

- event-driven decoupling is needed
- GCP-managed messaging is preferred
- Dataflow/Cloud Functions integrations are useful
- asynchronous processing fits

Compare:

- Kafka for broker ecosystem/control/replay patterns
- Pub/Sub for managed GCP-native messaging
- Cloud Tasks for task queue-like workloads

## 10. Trade-offs

| Pros | Cons |
|---|---|
| managed messaging | GCP-specific |
| decouples producers/consumers | idempotency required |
| integrates with Dataflow | ordering guarantees must be understood |
| supports push/pull | subscribers must handle redelivery |

## 11. Failure Modes

- Failure: Subscriber does not ack.
- Symptom: message redelivery.
- Recovery: fix subscriber and idempotency.
- Prevention: ack after durable processing.

- Failure: Bad message repeatedly fails.
- Symptom: poison message loop.
- Recovery: dead-letter topic.
- Prevention: schema validation.

- Failure: Subscriber lag grows.
- Symptom: stale downstream data.
- Recovery: scale subscribers.
- Prevention: lag/oldest message alerts.

## 12. Common Mistakes

- Mistake: Assuming exactly-once business effects.
- Why it is wrong: redelivery can happen.
- Better approach: idempotent consumers and dedupe keys.

- Mistake: One subscription shared by unrelated consumers.
- Why it is wrong: consumers compete instead of each getting all events.
- Better approach: use separate subscriptions per independent consumer group.

## 13. Mini Example

```text
topic: order-events
subscriptions:
  fraud-sub
  analytics-sub
  email-sub
```

## 14. Interview Questions

1. What is Pub/Sub?
2. Topic vs subscription?
3. What is ack/redelivery?
4. How do you handle poison messages?
5. Pub/Sub vs Kafka?

## 15. Interview Speak

"Pub/Sub is GCP's managed publish-subscribe messaging service. I would use it to decouple event producers and consumers, with separate subscriptions per consumer, idempotent processing, schema validation, dead-letter topics, and monitoring for delivery latency and backlog."

## 16. Quick Recall

- One-line summary: Pub/Sub decouples GCP event producers and subscribers.
- Three keywords: topic, subscription, ack.
- One trap: Forgetting redelivery/idempotency.
- One memory trick: Cloud mailbox for events.
