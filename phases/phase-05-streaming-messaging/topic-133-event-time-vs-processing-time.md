# Topic 133: Event Time Vs Processing Time

## 1. Goal

Understand the difference between when an event happened and when the system processed it.

## 2. Baby Intuition

Event time is when the photo was taken.

Processing time is when you uploaded the photo.

They can be different.

## 3. What It Is

- Simple definition: Event time is when the event occurred; processing time is when the system handles it.
- Technical definition: Event time is the timestamp embedded in the event from the source domain, while processing time is the stream processor's local clock time when processing occurs.
- Category: Stream-time semantics.
- Related terms: ingestion time, watermark, late event, window.

## 4. Why It Exists

Events can be delayed by:

- mobile offline mode
- network issues
- batching
- retries
- source outages
- clock skew

If analytics uses processing time, results may not match when things actually happened.

## 5. Where It Fits In A Data Platform

```text
source event timestamp -> event-time processing -> correct business windows
processor clock -> processing-time processing -> operational timing
```

## 6. How It Works Step By Step

Example event:

```json
{
  "event_time": "10:01",
  "received_at": "10:07"
}
```

Event-time window:

```text
counts event in 10:00-10:05 window
```

Processing-time window:

```text
counts event in 10:05-10:10 window
```

## 7. How To Use It Practically

Use event time for:

- user activity analytics
- financial event windows
- IoT readings
- sessionization
- correct historical reports

Use processing time for:

- system monitoring
- operational throughput
- simple low-latency approximations
- when event timestamp is unavailable/untrusted

## 8. Real-World Scenario

- Product/system: Mobile click analytics.
- Problem: User clicked at 9:58 but phone uploaded at 10:10.
- How event time helps: Count click in the correct 9:55-10:00 window.
- What would go wrong with processing time: metrics shift to the wrong time bucket.

## 9. System Design Angle

Event time improves correctness but needs:

- timestamps in events
- watermark strategy
- late event policy
- clock-quality thinking

Processing time is simpler but less accurate for business timing.

## 10. Trade-offs

| Event Time | Processing Time |
|---|---|
| business-correct windows | simpler and lower latency |
| handles delayed events | can misplace late events |
| needs watermarks | no event timestamp needed |
| more complex | easier operational metrics |

## 11. Failure Modes

- Failure: bad event timestamp.
- Symptom: event goes to wrong window.
- Recovery: validate or use ingestion time fallback.
- Prevention: timestamp quality checks.

- Failure: processing-time analytics for delayed data.
- Symptom: business metrics wrong by time bucket.
- Recovery: recompute with event time.
- Prevention: use event time where correctness matters.

## 12. Common Mistakes

- Mistake: Using processing time for business event analytics.
- Why it is wrong: delayed events go into wrong windows.
- Better approach: use event time plus watermarks.

- Mistake: Trusting client timestamps blindly.
- Why it is wrong: clocks can be wrong.
- Better approach: validate and record ingestion time too.

## 13. Mini Example

```text
event happened: 10:01
processed: 10:07

event-time result -> 10:00 window
processing-time result -> 10:05 window
```

## 14. Interview Questions

1. Event time vs processing time?
2. Why does event time matter?
3. What causes late events?
4. When is processing time okay?
5. How do watermarks relate?

## 15. Interview Speak

"Event time is when the event actually happened, while processing time is when the stream processor sees it. For business analytics and windows, event time is usually more correct, but it requires reliable timestamps, watermarks, and late-event handling."

## 16. Quick Recall

- One-line summary: Event time is happened time; processing time is handled time.
- Three keywords: timestamp, watermark, late.
- One trap: Using processing time for delayed business events.
- One memory trick: Photo taken vs photo uploaded.
