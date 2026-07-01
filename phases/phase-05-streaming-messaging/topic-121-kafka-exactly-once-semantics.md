# Topic 121: Kafka Exactly-Once Semantics

## 1. Goal

Understand Kafka exactly-once semantics without falling for the myth that duplicates disappear everywhere.

## 2. Baby Intuition

Exactly-once in Kafka is like a carefully tracked bank transfer inside a controlled system.

It can make the final Kafka-to-Kafka result appear once, but outside systems still need careful handling.

## 3. What It Is

- Simple definition: Kafka exactly-once semantics help ensure records are processed and written once in Kafka transactions.
- Technical definition: Kafka exactly-once semantics combine idempotent producers and transactions so consume-process-produce workflows can atomically commit output records and input offsets.
- Category: Kafka processing guarantee.
- Related terms: idempotent producer, transaction, transactional id, offset commit, Kafka Streams.

## 4. Why It Exists

At-least-once processing can duplicate outputs.

Example:

```text
consume event -> write output -> crash before committing offset -> reprocess -> duplicate output
```

EOS exists to make Kafka-based pipelines safer when reading from Kafka and writing back to Kafka.

## 5. Where It Fits In A Data Platform

```text
Kafka input topic -> stream processor -> Kafka output topic
```

EOS is strongest when source and sink are Kafka and transactions are used.

## 6. How It Works Step By Step

1. Producer enables idempotence.
2. Processor begins transaction.
3. Processor reads input records.
4. Processor writes output records.
5. Processor sends consumed offsets as part of transaction.
6. Transaction commits atomically.
7. Consumers with correct isolation read committed results.

If failure happens before commit:

```text
transaction aborts, output is not visible as committed
```

## 7. How To Use It Practically

Producer configs:

```properties
enable.idempotence=true
transactional.id=my-app-1
acks=all
```

Consumer isolation:

```properties
isolation.level=read_committed
```

Kafka Streams:

```properties
processing.guarantee=exactly_once_v2
```

## 8. Real-World Scenario

- Product/system: Stream aggregation from Kafka topic to Kafka topic.
- Problem: Count events without duplicate output after processor restart.
- How EOS helps: Output records and consumed offsets commit atomically.
- What would go wrong without it: restart could duplicate aggregate updates.

## 9. System Design Angle

EOS is valuable when:

- source is Kafka
- sink is Kafka
- processing framework supports transactions
- duplicates are costly

Be careful when sink is:

- database
- email service
- external API
- payment processor

External side effects need idempotency or their own transaction strategy.

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| stronger Kafka-to-Kafka correctness | transaction overhead |
| fewer duplicate outputs | configuration complexity |
| atomic offset/output commit | not universal for external sinks |
| safer stream processing | operational understanding needed |

## 11. Failure Modes

- Failure: external sink duplicates.
- Symptom: DB/API sees repeated writes despite Kafka EOS.
- Recovery: dedupe/idempotent sink.
- Prevention: use idempotency keys.

- Failure: wrong isolation level.
- Symptom: consumers see uncommitted/aborted records.
- Recovery: set `read_committed`.
- Prevention: configure consumers correctly.

## 12. Common Mistakes

- Mistake: Saying EOS means no duplicates anywhere.
- Why it is wrong: guarantee scope matters.
- Better approach: specify Kafka-to-Kafka transactional boundary.

- Mistake: Ignoring idempotency with external systems.
- Why it is wrong: external side effects may repeat.
- Better approach: design idempotent writes.

## 13. Mini Example

Safe Kafka transaction:

```text
read input offsets 10-20
write output events
commit output + offsets together
```

Either both commit or neither commits.

## 14. Interview Questions

1. What is Kafka exactly-once semantics?
2. What problem does idempotent producer solve?
3. What do transactions add?
4. Does EOS apply to external databases?
5. What is `read_committed`?

## 15. Interview Speak

"Kafka exactly-once semantics combine idempotent producers and transactions so Kafka input offsets and Kafka output records can be committed atomically. It is strongest for Kafka-to-Kafka pipelines. For external sinks, I still design idempotent writes because Kafka EOS does not automatically make external side effects exactly once."

## 16. Quick Recall

- One-line summary: Kafka EOS is transactional correctness within Kafka boundaries.
- Three keywords: idempotence, transaction, offsets.
- One trap: Claiming no duplicates anywhere.
- One memory trick: Exactly once inside the fenced garden.
