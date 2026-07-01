# Topic 132: Flink Watermarks

## 1. Goal

Understand watermarks as Flink's way to track progress of event time.

## 2. Baby Intuition

Imagine waiting for mail from yesterday.

At some point, you say:

```text
Most mail up to 5 PM has probably arrived. I can process that window now.
```

That signal is like a watermark.

## 3. What It Is

- Simple definition: A watermark tells Flink how far event time has progressed.
- Technical definition: A watermark is a timestamp marker indicating that the system does not expect events with event time earlier than that timestamp, except as configured late data.
- Category: Event-time stream processing.
- Related terms: event time, processing time, window, late event, allowed lateness.

## 4. Why It Exists

Events arrive out of order.

Example:

```text
event happened at 10:01
arrives at 10:05
```

Flink needs to know when to close event-time windows despite out-of-order arrivals.

Watermarks solve this.

## 5. Where It Fits In A Data Platform

```text
events with timestamps -> watermark strategy -> event-time windows -> output
```

Used in:

- windowed aggregations
- session windows
- late event handling
- event-time joins

## 6. How It Works Step By Step

1. Events arrive with event timestamps.
2. Watermark generator observes timestamps.
3. It emits watermark like `10:05`.
4. Flink treats event time up to watermark as mostly complete.
5. Windows ending before watermark can close.
6. Later older events are considered late.

## 7. How To Use It Practically

Watermark strategy examples:

```text
bounded out-of-orderness: allow events to arrive up to 5 minutes late
```

Meaning:

```text
watermark = max_event_time_seen - 5 minutes
```

If max event time is 10:10, watermark is 10:05.

## 8. Real-World Scenario

- Product/system: Mobile analytics.
- Problem: Phones send events late due to poor network.
- How watermarks help: Wait a reasonable delay before finalizing windows.
- What would go wrong without them: windows close too early and miss late mobile events.

## 9. System Design Angle

Watermark choice is a business trade-off:

```text
longer delay -> more complete results, higher latency
shorter delay -> faster results, more late/missing events
```

Ask:

- how late can events arrive?
- how fresh must output be?
- are late corrections allowed?
- what happens to very late events?

## 10. Trade-offs

| Longer Watermark Delay | Shorter Watermark Delay |
|---|---|
| more complete windows | lower latency |
| fewer late events | more missing/late corrections |
| slower dashboards | fresher dashboards |

## 11. Failure Modes

- Failure: watermark stuck.
- Symptom: windows do not emit.
- Recovery: handle idle sources.
- Prevention: configure idleness.

- Failure: watermark too aggressive.
- Symptom: many late events.
- Recovery: increase allowed delay.
- Prevention: analyze event lateness.

## 12. Common Mistakes

- Mistake: Confusing watermark with current processing time.
- Why it is wrong: watermark tracks event-time progress.
- Better approach: distinguish event time vs processing time.

- Mistake: Setting watermark without data analysis.
- Why it is wrong: lateness patterns vary.
- Better approach: measure event delay distribution.

## 13. Mini Example

```text
max event time seen: 10:10
allowed out-of-order delay: 5 minutes
watermark: 10:05
```

## 14. Interview Questions

1. What is a watermark?
2. Why are watermarks needed?
3. How do watermarks handle out-of-order events?
4. What happens if watermark is too aggressive?
5. Why can watermarks get stuck?

## 15. Interview Speak

"A watermark is Flink's event-time progress signal. It tells the engine when it is reasonable to close event-time windows even though events can arrive out of order. Watermark delay trades result completeness for latency, so I choose it based on observed lateness and business freshness needs."

## 16. Quick Recall

- One-line summary: Watermark says how far event time has probably progressed.
- Three keywords: event time, windows, lateness.
- One trap: Confusing watermark with wall-clock time.
- One memory trick: Time marker for "we have probably seen enough."
