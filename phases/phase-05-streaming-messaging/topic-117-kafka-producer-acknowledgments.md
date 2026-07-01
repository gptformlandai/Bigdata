# Topic 117: Kafka Producer Acknowledgments

## 1. Goal

Understand producer acknowledgments as the write durability setting for Kafka producers.

## 2. Baby Intuition

When you hand in an assignment, you may want confirmation.

- no confirmation: fastest, risky
- teacher confirms: better
- teacher and backup copies confirm: safest

Kafka producer acknowledgments work similarly.

## 3. What It Is

- Simple definition: Producer acks control when Kafka says a write succeeded.
- Technical definition: The `acks` producer setting determines how many broker replicas must acknowledge a record before the producer considers it successful.
- Category: Kafka producer reliability.
- Related terms: acks=0, acks=1, acks=all, retries, idempotent producer, min.insync.replicas.

## 4. Why It Exists

Different events have different durability needs.

Metrics debug event:

```text
maybe okay to lose rarely
```

Payment event:

```text
must not lose after success
```

Acks let producers choose latency vs durability.

## 5. Where It Fits In A Data Platform

```text
Producer -> broker leader -> replicas -> producer ack
```

Ack setting is on the producer side but depends on broker/topic replication.

## 6. How It Works Step By Step

`acks=0`:

1. Producer sends record.
2. Does not wait for broker response.
3. Fastest, possible loss.

`acks=1`:

1. Producer sends record to leader.
2. Leader writes and responds.
3. Followers may not have it yet.

`acks=all`:

1. Producer sends record to leader.
2. Leader waits for in-sync replicas based on min ISR.
3. Producer gets success only after stronger replication.

## 7. How To Use It Practically

Reliable producer config:

```properties
acks=all
enable.idempotence=true
retries=2147483647
max.in.flight.requests.per.connection=5
```

Critical topics often use:

```properties
min.insync.replicas=2
replication.factor=3
```

## 8. Real-World Scenario

- Product/system: Payment event producer.
- Problem: Do not acknowledge success unless event is safely replicated.
- How acks help: `acks=all` waits for in-sync replicas.
- What would go wrong with weak acks: a broker crash could lose acknowledged payment events.

## 9. System Design Angle

Ack setting affects:

- producer latency
- durability
- availability
- error rate under replica failure

For critical data:

```text
acks=all + idempotent producer + RF 3 + min ISR 2
```

For low-value telemetry:

```text
acks=1 may be acceptable
```

## 10. Trade-offs

| Setting | Gain | Risk |
|---|---|---|
| acks=0 | lowest latency | highest loss risk |
| acks=1 | leader durability | loss if leader dies before replication |
| acks=all | strongest durability | higher latency and possible failures |

## 11. Failure Modes

- Failure: not enough ISR with `acks=all`.
- Symptom: producer errors.
- Recovery: restore replicas.
- Prevention: broker health and ISR monitoring.

- Failure: retries without idempotence.
- Symptom: duplicate records.
- Recovery: dedupe downstream.
- Prevention: enable idempotent producer.

## 12. Common Mistakes

- Mistake: Using `acks=1` for critical financial events.
- Why it is wrong: acknowledged write may be lost if leader fails before replication.
- Better approach: use `acks=all` with min ISR.

- Mistake: Thinking acks solves consumer processing.
- Why it is wrong: acks only covers producer write success.
- Better approach: separately design consumer delivery semantics.

## 13. Mini Example

```text
acks=all, RF=3, min ISR=2

write succeeds if leader and at least one other in-sync replica have the record.
```

## 14. Interview Questions

1. What does `acks` control?
2. Difference between `acks=0`, `1`, and `all`?
3. How does `min.insync.replicas` affect writes?
4. Why enable idempotent producer?
5. How do acks affect latency?

## 15. Interview Speak

"Kafka producer acknowledgments control when a produce request is considered successful. `acks=1` waits for the leader only, while `acks=all` waits for in-sync replicas based on topic settings like `min.insync.replicas`. For critical data, I would use `acks=all`, RF 3, min ISR 2, retries, and idempotent producer."

## 16. Quick Recall

- One-line summary: Acks decide how safely Kafka confirms writes.
- Three keywords: producer, acks, ISR.
- One trap: Strong producer acks do not guarantee consumer success.
- One memory trick: How many people confirm they copied the note?
