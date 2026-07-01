# Topic 134: Windowing

## 1. Goal

Understand windows as a way to group infinite streams into finite time ranges.

## 2. Baby Intuition

A stream never ends.

To count events, you need to ask:

```text
count over which time range?
```

A window gives that time range.

## 3. What It Is

- Simple definition: Windowing groups stream events into time-based buckets.
- Technical definition: Windowing splits unbounded streams into finite logical intervals for aggregation, joins, and analysis.
- Category: Stream processing operation.
- Related terms: tumbling window, sliding window, session window, watermark, late event.

## 4. Why It Exists

Batch data has natural boundaries:

```text
yesterday's file
```

Streams do not.

Windows exist so we can compute:

- clicks per minute
- revenue per hour
- active users per 5 minutes
- fraud attempts in last 10 minutes

## 5. Where It Fits In A Data Platform

```text
event stream -> keyBy -> window -> aggregate -> output
```

## 6. How It Works Step By Step

Tumbling window:

```text
10:00-10:05
10:05-10:10
10:10-10:15
```

Sliding window:

```text
size 10 minutes, slide 5 minutes
10:00-10:10
10:05-10:15
10:10-10:20
```

Session window:

```text
group events separated by less than inactivity gap
```

## 7. How To Use It Practically

Common choices:

- tumbling: fixed non-overlapping windows
- sliding: overlapping rolling metrics
- session: user activity sessions

Design:

```text
window length + slide + event time + watermark + late event policy
```

## 8. Real-World Scenario

- Product/system: Real-time dashboard.
- Problem: Show purchases per minute.
- How windowing helps: Count purchase events in one-minute windows.
- What would go wrong without it: stream is infinite, so aggregation boundary is unclear.

## 9. System Design Angle

Window choice affects:

- latency
- correctness
- compute cost
- state size
- dashboard behavior

Longer windows:

- more state
- smoother metrics
- more latency for final results

Shorter windows:

- fresher
- noisier
- more output frequency

## 10. Trade-offs

| Window Type | Good For | Cost |
|---|---|---|
| tumbling | simple periodic metrics | fixed boundaries |
| sliding | rolling metrics | more computation |
| session | user behavior | state and gap tuning |

## 11. Failure Modes

- Failure: wrong window type.
- Symptom: metric does not match business meaning.
- Recovery: redesign windows.
- Prevention: define metric carefully.

- Failure: window state grows.
- Symptom: memory/checkpoint pressure.
- Recovery: shorter windows/TTL.
- Prevention: estimate cardinality and window size.

## 12. Common Mistakes

- Mistake: Windowing by processing time when event time is needed.
- Why it is wrong: late events go to wrong window.
- Better approach: event-time windows with watermarks.

- Mistake: Choosing too many overlapping windows.
- Why it is wrong: compute/state cost grows.
- Better approach: use only needed granularity.

## 13. Mini Example

```text
Events at 10:01, 10:02, 10:06

5-minute tumbling:
10:00-10:05 -> 2 events
10:05-10:10 -> 1 event
```

## 14. Interview Questions

1. What is windowing?
2. Tumbling vs sliding vs session windows?
3. Why do streams need windows?
4. How do watermarks affect windows?
5. How does window size affect state?

## 15. Interview Speak

"Windowing turns an unbounded stream into finite time ranges for aggregation. Tumbling windows are fixed and non-overlapping, sliding windows overlap, and session windows group activity by inactivity gaps. Window design depends on event time, watermarks, late-event policy, state size, and metric meaning."

## 16. Quick Recall

- One-line summary: Windows give time boundaries to infinite streams.
- Three keywords: tumbling, sliding, session.
- One trap: wrong time semantics.
- One memory trick: Slice the river into time buckets.
