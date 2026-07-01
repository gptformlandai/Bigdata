# Topic 113: Kafka Offset

## 1. Goal

Understand offsets as Kafka's position numbers inside partitions.

## 2. Baby Intuition

An offset is like a page number in a partition's notebook.

Consumers remember which page they have read up to.

## 3. What It Is

- Simple definition: An offset is the position of a record in a Kafka partition.
- Technical definition: A Kafka offset is a monotonically increasing number assigned to each record within a partition, used by consumers to track read progress.
- Category: Kafka consumption/progress tracking.
- Related terms: partition, consumer, commit, lag, replay.

## 4. Why It Exists

Kafka needs a way to know:

- where each record is
- what a consumer has read
- where to resume after failure
- how to replay old data
- how far behind a consumer is

Offsets solve this by numbering records per partition.

## 5. Where It Fits In A Data Platform

```text
Topic partition -> records with offsets -> consumer commits offset
```

Offsets are tracked per:

```text
consumer group + topic + partition
```

## 6. How It Works Step By Step

1. Producer appends record to partition.
2. Kafka assigns next offset.
3. Consumer reads record.
4. Consumer processes record.
5. Consumer commits offset.
6. After restart, consumer resumes from committed offset.

## 7. How To Use It Practically

Consumer group offsets:

```bash
kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group analytics
```

You may see:

```text
CURRENT-OFFSET
LOG-END-OFFSET
LAG
```

Replay idea:

```text
reset offsets to earlier position, then reprocess retained events
```

## 8. Real-World Scenario

- Product/system: Data lake Kafka consumer.
- Problem: Consumer crashes after reading events.
- How offsets help: It resumes from last committed offset.
- What would go wrong without offsets: Consumer would not know where to restart.

## 9. System Design Angle

Offset commit timing affects delivery semantics:

- commit before processing -> possible data loss
- commit after processing -> possible duplicates

Most reliable pipelines:

```text
process successfully -> commit offset
```

Then design idempotent sinks.

## 10. Trade-offs

| Commit Strategy | Trade-off |
|---|---|
| before processing | lower duplicate risk, higher loss risk |
| after processing | lower loss risk, higher duplicate risk |
| transactional commit | stronger guarantee, more complexity |

## 11. Failure Modes

- Failure: commit too early.
- Symptom: message lost if processing fails.
- Recovery: hard if no replay from earlier offset.
- Prevention: commit after successful processing.

- Failure: commit too late.
- Symptom: duplicate processing.
- Recovery: idempotent writes.
- Prevention: careful commit strategy.

## 12. Common Mistakes

- Mistake: Thinking offset is global across topic.
- Why it is wrong: offsets are per partition.
- Better approach: identify topic-partition-offset.

- Mistake: Auto-commit without understanding.
- Why it is wrong: can commit messages before safe processing.
- Better approach: choose commit behavior intentionally.

## 13. Mini Example

```text
partition 0:
offset 0 -> event A
offset 1 -> event B
offset 2 -> event C
```

Consumer committed offset 2 means it has progressed to that point depending on client semantics.

## 14. Interview Questions

1. What is a Kafka offset?
2. Are offsets global?
3. How do consumers use offsets?
4. How does offset commit affect duplicates/loss?
5. What is lag?

## 15. Interview Speak

"A Kafka offset is a record position within a partition. Consumers track and commit offsets per consumer group, topic, and partition. Offset commit timing controls recovery behavior: committing after processing avoids loss but can create duplicates, so sinks should be idempotent."

## 16. Quick Recall

- One-line summary: Offset is a consumer's page number in a partition.
- Three keywords: partition, commit, replay.
- One trap: Thinking offsets are topic-global.
- One memory trick: Offset is the bookmark.
