# Topic 111: Kafka Topic

## 1. Goal

Understand topics as named streams where Kafka events are published.

## 2. Baby Intuition

A topic is like a folder or channel for one kind of event.

Orders go to an `orders` topic. Clicks go to a `clicks` topic. Payments go to a `payments` topic.

## 3. What It Is

- Simple definition: A topic is a named stream of records.
- Technical definition: A Kafka topic is a logical category of records, split into partitions and stored on brokers.
- Category: Kafka data organization.
- Related terms: partition, producer, consumer, retention, replication.

## 4. Why It Exists

Kafka needs a way to organize events by purpose.

Without topics:

- all events are mixed together
- consumers cannot subscribe cleanly
- retention/settings cannot be controlled by stream
- ownership is unclear

## 5. Where It Fits In A Data Platform

```text
Producer -> Topic -> Consumer groups
```

Examples:

- `orders.created`
- `payments.authorized`
- `clickstream.events`
- `dbserver.inventory.products`

## 6. How It Works Step By Step

1. Topic is created with partition count and replication factor.
2. Producers send records to topic.
3. Kafka writes records to one of the topic's partitions.
4. Consumers subscribe to topic.
5. Consumers read partitions by offset.

## 7. How To Use It Practically

Create topic:

```bash
kafka-topics --bootstrap-server localhost:9092 --create --topic clickstream.events --partitions 6 --replication-factor 3
```

List topics:

```bash
kafka-topics --bootstrap-server localhost:9092 --list
```

Describe topic:

```bash
kafka-topics --bootstrap-server localhost:9092 --describe --topic clickstream.events
```

## 8. Real-World Scenario

- Product/system: Clickstream analytics.
- Problem: Websites publish every user click.
- How topic helps: All click events are organized in `clickstream.events`.
- What would go wrong without it: Consumers would need to filter a mixed global event stream.

## 9. System Design Angle

Topic design affects:

- ownership
- retention
- partition count
- schema
- access control
- consumer contracts

Good topic names are clear and stable.

Avoid:

- one topic for everything
- too many tiny topics without reason
- topic names tied to temporary implementation details

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| event organization | topic governance |
| independent retention/config | more metadata |
| cleaner consumer subscriptions | naming/versioning decisions |

## 11. Failure Modes

- Failure: Wrong topic retention.
- Symptom: events deleted too early or storage grows too much.
- Recovery: adjust retention.
- Prevention: set retention by use case.

- Failure: Bad topic ownership.
- Symptom: schema changes break consumers.
- Recovery: governance and contracts.
- Prevention: owner and schema rules.

## 12. Common Mistakes

- Mistake: Putting unrelated events in one topic.
- Why it is wrong: schemas and consumers become messy.
- Better approach: group events by domain and access pattern.

- Mistake: Creating topic per user.
- Why it is wrong: topic metadata explodes.
- Better approach: partition by user key within a topic.

## 13. Mini Example

```text
Topic: orders.events
Events:
  OrderCreated
  OrderCancelled
  OrderShipped
```

## 14. Interview Questions

1. What is a Kafka topic?
2. How is a topic different from a partition?
3. How do you choose topic names?
4. Why not create one topic per user?
5. What configs are topic-level?

## 15. Interview Speak

"A Kafka topic is a named stream of records. Producers write records to topics, and consumers subscribe to topics. Internally, topics are split into partitions for scale and ordering. Topic design should consider ownership, schema, retention, partition count, and access patterns."

## 16. Quick Recall

- One-line summary: Topic is a named event stream.
- Three keywords: stream, partitions, retention.
- One trap: Topic per user.
- One memory trick: Topic is an event channel.
