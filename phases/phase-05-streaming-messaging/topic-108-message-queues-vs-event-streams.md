# Topic 108: Message Queues Vs Event Streams

## 1. Goal

Understand the difference between message queues and event streams, and when to use each.

## 2. Baby Intuition

A queue is like a task inbox.

One worker takes a task, does it, and the task is gone.

An event stream is like a recorded timeline.

Many readers can read the same timeline at their own pace, and old events can be replayed while retained.

## 3. What It Is

- Simple definition: Queues distribute work; streams store ordered event logs for multiple consumers.
- Technical definition: A message queue typically delivers messages to competing consumers for task processing, while an event stream stores append-only records that consumers read by offset and can replay.
- Category: Messaging/streaming architecture.
- Related terms: broker, topic, partition, offset, consumer group, retention, pub/sub.

## 4. Why It Exists

Different problems need different messaging patterns.

Queue problem:

```text
I have tasks. I need workers to process each task once.
```

Stream problem:

```text
I have events. Many systems need to read the same history independently.
```

## 5. Where It Fits In A Data Platform

Queue:

```text
API -> queue -> workers -> database/email/payment
```

Stream:

```text
apps -> Kafka topic -> analytics/fraud/search/data lake consumers
```

## 6. How It Works Step By Step

Queue flow:

1. Producer sends message.
2. Queue stores message.
3. One worker consumes message.
4. Worker acknowledges success.
5. Message is removed or hidden permanently.

Stream flow:

1. Producer appends event to stream.
2. Stream stores event for retention period.
3. Consumers read using offsets.
4. Different consumer groups read independently.
5. Consumers can replay old offsets if data is retained.

## 7. How To Use It Practically

Use a queue for:

- background jobs
- email sending
- image processing
- task distribution
- work that should be handled by one worker

Use a stream for:

- clickstream analytics
- CDC
- real-time dashboards
- fraud signals
- logs/metrics pipelines
- multiple independent consumers

Example tools:

| Pattern | Tools |
|---|---|
| Queue | RabbitMQ, SQS, Celery queues |
| Stream | Kafka, Kinesis, Pub/Sub, Pulsar |

## 8. Real-World Scenario

- Product/system: E-commerce.
- Queue use: Send order confirmation emails.
- Stream use: Publish order events for analytics, fraud, inventory, and recommendations.
- What would go wrong if confused: A queue may remove messages before all analytics consumers read them; a stream may be overkill for simple one-worker tasks.

## 9. System Design Angle

Ask:

- Does every message need one worker or many consumers?
- Do we need replay?
- Do we need ordered history?
- How long should data be retained?
- Is this task processing or event history?

Interview keywords:

- "background job" -> queue
- "replayable events" -> stream
- "multiple independent consumers" -> stream
- "work distribution" -> queue

## 10. Trade-offs

| Queue | Stream |
|---|---|
| simple task distribution | replayable event history |
| message usually removed after ack | retained for time/size |
| great for worker pools | great for analytics/fan-out |
| less natural replay | requires offset management |

## 11. Failure Modes

- Failure: Queue worker crashes before ack.
- Symptom: message becomes visible again or is retried.
- Recovery: retry or DLQ.
- Prevention: idempotent workers.

- Failure: Stream consumer falls behind.
- Symptom: consumer lag grows.
- Recovery: scale/tune consumers.
- Prevention: monitor lag and throughput.

## 12. Common Mistakes

- Mistake: Using a queue when many consumers need the same event.
- Why it is wrong: one consumer may take/remove the message.
- Better approach: use event stream/pub-sub.

- Mistake: Using a stream for simple one-off work with no replay need.
- Why it is wrong: adds operational complexity.
- Better approach: use a queue.

## 13. Mini Example

```text
Queue:
message A -> worker 1 processes it

Stream:
event A -> analytics reads it
        -> fraud reads it
        -> data lake writer reads it
```

## 14. Interview Questions

1. Queue vs stream?
2. When would you use Kafka instead of RabbitMQ/SQS?
3. What is replay?
4. What is a consumer group?
5. Why does retention matter?

## 15. Interview Speak

"Queues are best for task distribution where one worker should process a message. Event streams are append-only logs where multiple consumer groups can independently read and replay events by offset. For real-time analytics or CDC, I would choose a stream; for background jobs like email sending, a queue may be simpler."

## 16. Quick Recall

- One-line summary: Queue is task inbox; stream is replayable timeline.
- Three keywords: ack, offset, replay.
- One trap: Using queue when many systems need the same event.
- One memory trick: Inbox vs timeline.
