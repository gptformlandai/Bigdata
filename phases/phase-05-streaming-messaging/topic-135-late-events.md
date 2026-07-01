# Topic 135: Late Events

## 1. Goal

Understand late events and how streaming systems handle data that arrives after its event-time window.

## 2. Baby Intuition

A student submits homework after the teacher has already graded the class.

The teacher needs a policy:

- accept and update grade
- accept only within 1 day
- reject as too late

Streaming systems need the same policy.

## 3. What It Is

- Simple definition: A late event arrives after the system expected its event-time window to be complete.
- Technical definition: Late events are records whose event timestamps are earlier than the current watermark or window close threshold.
- Category: Event-time stream processing issue.
- Related terms: watermark, allowed lateness, side output, correction, retraction.

## 4. Why It Exists

Events arrive late because of:

- mobile offline mode
- retries
- network delay
- source batching
- outages
- clock skew
- backpressure

Late events are normal in real systems.

## 5. Where It Fits In A Data Platform

```text
event-time window + watermark -> late event policy
```

Late-event handling affects dashboards, alerts, and correctness.

## 6. How It Works Step By Step

Example:

```text
window: 10:00-10:05
watermark passes 10:05
window emits result
event with timestamp 10:03 arrives at 10:08
```

That event is late.

Options:

1. Drop it.
2. Send to side output/DLQ.
3. Update previous result.
4. Emit correction/retraction.
5. Store for batch reconciliation.

## 7. How To Use It Practically

Design policy:

```text
allowed lateness = 5 minutes
events later than that -> late-events topic/table
```

Also store:

- event time
- processing time
- delay
- reason if dropped

## 8. Real-World Scenario

- Product/system: Mobile app analytics.
- Problem: Users go offline and upload events later.
- How late handling helps: Accept events up to a delay and correct windows.
- What would go wrong without it: reports undercount mobile behavior.

## 9. System Design Angle

Late-event policy is business-specific.

Fraud detection:

- very late events may be useless for immediate blocking but useful for audit.

Finance reporting:

- late events may require corrections.

Dashboard:

- may show "preliminary" and later update.

## 10. Trade-offs

| More Lateness Allowed | Less Lateness Allowed |
|---|---|
| more complete results | lower latency |
| more state retained | less memory/state |
| more corrections | simpler outputs |

## 11. Failure Modes

- Failure: dropping important late events.
- Symptom: incorrect metrics.
- Recovery: batch backfill/reconciliation.
- Prevention: measure lateness and set policy.

- Failure: allowing too much lateness.
- Symptom: large state and slow checkpoints.
- Recovery: reduce allowed lateness.
- Prevention: balance correctness vs cost.

## 12. Common Mistakes

- Mistake: Treating late events as rare edge cases.
- Why it is wrong: real networks and mobile clients produce late events constantly.
- Better approach: design policy from day one.

- Mistake: No correction strategy.
- Why it is wrong: outputs may be wrong forever.
- Better approach: side outputs, retractions, or reconciliation.

## 13. Mini Example

```text
allowed lateness: 5 minutes
event time: 10:03
watermark: 10:07

event is still accepted.

watermark: 10:20
same event is too late.
```

## 14. Interview Questions

1. What is a late event?
2. How do watermarks define lateness?
3. What can you do with late events?
4. How does allowed lateness affect state?
5. How would you handle late events in dashboards?

## 15. Interview Speak

"Late events are events that arrive after their event-time window is considered complete, usually based on watermarks. I would define allowed lateness based on business needs, then either update results, emit corrections, send very late events to side output/DLQ, or reconcile later in batch."

## 16. Quick Recall

- One-line summary: Late events arrive after their event-time window.
- Three keywords: watermark, allowed lateness, correction.
- One trap: Dropping late data without business agreement.
- One memory trick: Homework after grading time.
