# Topic 118: Kafka Retention

## 1. Goal

Understand retention as Kafka's rule for how long records are kept.

## 2. Baby Intuition

Kafka is not infinite storage.

Retention is the cleanup rule:

```text
keep events for 7 days
or keep until topic reaches size limit
```

## 3. What It Is

- Simple definition: Retention controls when Kafka deletes old records.
- Technical definition: Kafka retention policies delete log segments based on time, size, or compaction settings.
- Category: Kafka storage lifecycle.
- Related terms: log segment, retention.ms, retention.bytes, cleanup policy, replay.

## 4. Why It Exists

Kafka stores events on broker disks.

Without retention:

- disks fill
- brokers fail
- costs grow forever

Retention balances replay needs with storage cost.

## 5. Where It Fits In A Data Platform

```text
Kafka topic -> retained event log -> consumers can replay while data remains
```

If data expires before consumer reads it, it is gone from Kafka.

## 6. How It Works Step By Step

1. Kafka writes records to log segments.
2. Segments age and grow.
3. Kafka checks retention rules.
4. Old/large segments become eligible for deletion.
5. Disk space is freed.

Retention is not per consumed message. Kafka does not delete immediately after a consumer reads.

## 7. How To Use It Practically

Topic config examples:

```bash
kafka-configs --bootstrap-server localhost:9092 --alter --entity-type topics --entity-name clicks --add-config retention.ms=604800000
```

7 days:

```text
604800000 ms
```

Size retention:

```properties
retention.bytes=107374182400
```

## 8. Real-World Scenario

- Product/system: Clickstream stream.
- Problem: Consumers may need to replay last 3 days after a bug.
- How retention helps: Keep events long enough for replay/backfill.
- What would go wrong with too-short retention: bug fix cannot replay lost processing window.

## 9. System Design Angle

Retention affects:

- replay window
- storage cost
- disaster recovery
- consumer lag tolerance
- compliance/privacy

Ask:

- how long might consumers be down?
- how far back do we need replay?
- how much data per day?
- what is disk capacity?
- are events sensitive?

## 10. Trade-offs

| Longer Retention | Shorter Retention |
|---|---|
| more replay ability | lower storage cost |
| more lag tolerance | less recovery window |
| easier backfills | higher loss risk after outage |

## 11. Failure Modes

- Failure: retention too short.
- Symptom: consumer cannot catch up; offsets out of range.
- Recovery: restore from data lake/source if available.
- Prevention: set retention based on recovery needs.

- Failure: retention too long for disk.
- Symptom: broker disk fills.
- Recovery: increase storage or reduce retention.
- Prevention: capacity planning.

## 12. Common Mistakes

- Mistake: Thinking Kafka deletes after consumer reads.
- Why it is wrong: retention is time/size based, not per-consumer.
- Better approach: understand retained log model.

- Mistake: Setting retention without data volume math.
- Why it is wrong: disk may fill.
- Better approach: estimate daily GB * retention * replication factor.

## 13. Mini Example

```text
100 GB/day topic
7 day retention
RF=3

Approx storage = 100 * 7 * 3 = 2100 GB
```

## 14. Interview Questions

1. What is Kafka retention?
2. Is data deleted when consumed?
3. How does retention affect replay?
4. How do you size storage?
5. What happens if consumer is behind beyond retention?

## 15. Interview Speak

"Kafka retention controls how long records remain in a topic based on time or size. Kafka does not delete messages just because a consumer read them. Retention determines replay window, lag tolerance, and storage cost, so I size it using data volume, replication factor, recovery needs, and compliance rules."

## 16. Quick Recall

- One-line summary: Retention is Kafka's event cleanup window.
- Three keywords: time, size, replay.
- One trap: Thinking consumed messages disappear.
- One memory trick: Kafka keeps pages until cleanup day.
