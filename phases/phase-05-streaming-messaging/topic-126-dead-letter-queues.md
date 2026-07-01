# Topic 126: Dead Letter Queues

## 1. Goal

Understand dead letter queues as a safe place for records that cannot be processed normally.

## 2. Baby Intuition

If a package has a bad address, the delivery person should not stop delivering every package.

They put the bad package in an exception bin.

That exception bin is a DLQ.

## 3. What It Is

- Simple definition: A DLQ stores failed or poison messages for later inspection.
- Technical definition: A dead letter queue/topic is a separate destination for records that fail processing after validation, parsing, or retry rules.
- Category: Error handling pattern.
- Related terms: poison message, retry, quarantine, bad records, error topic.

## 4. Why It Exists

One bad record should not stop the entire stream.

DLQs help with:

- malformed JSON/Avro
- schema mismatches
- invalid values
- processing exceptions
- non-retryable errors

## 5. Where It Fits In A Data Platform

```text
Kafka topic -> consumer/processor
  -> valid records -> output
  -> bad records -> DLQ
```

DLQ is usually another Kafka topic or storage table.

## 6. How It Works Step By Step

1. Consumer reads record.
2. Consumer tries to parse/validate/process.
3. If record fails with non-retryable error, write to DLQ.
4. Include error reason and original record.
5. Commit original offset if safe.
6. Team investigates and reprocesses/fixes later.

## 7. How To Use It Practically

DLQ record should include:

```json
{
  "original_topic": "orders",
  "partition": 0,
  "offset": 123,
  "error": "missing required field amount",
  "original_payload": "{...}"
}
```

Practical rule:

```text
DLQ is not a trash can. Monitor it.
```

## 8. Real-World Scenario

- Product/system: Order analytics consumer.
- Problem: Some events miss required `order_id`.
- How DLQ helps: Bad events go to DLQ while valid events continue processing.
- What would go wrong without it: one poison event can block the consumer repeatedly.

## 9. System Design Angle

DLQs are useful when:

- malformed records are possible
- stream must keep moving
- bad records need investigation
- replay/reprocessing is needed

Design questions:

- what errors go to DLQ?
- how many retries first?
- who owns DLQ monitoring?
- how are DLQ records replayed?
- how long are DLQ records retained?

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| pipeline keeps moving | bad data delayed |
| easier debugging | DLQ monitoring needed |
| preserves failed records | replay tooling needed |
| avoids poison-message loops | risk of hiding data quality issues |

## 11. Failure Modes

- Failure: DLQ not monitored.
- Symptom: bad records pile up silently.
- Recovery: alert and process backlog.
- Prevention: DLQ metrics and ownership.

- Failure: retryable error sent to DLQ too quickly.
- Symptom: unnecessary manual work.
- Recovery: reprocess.
- Prevention: classify retryable vs non-retryable errors.

## 12. Common Mistakes

- Mistake: Swallowing bad records without saving them.
- Why it is wrong: data loss and no debugging.
- Better approach: write to DLQ with context.

- Mistake: Retrying poison messages forever.
- Why it is wrong: consumer gets stuck.
- Better approach: bounded retries then DLQ.

## 13. Mini Example

```text
orders topic:
good event -> output table
bad event -> orders.dlq topic
```

## 14. Interview Questions

1. What is a DLQ?
2. What is a poison message?
3. What should a DLQ record contain?
4. When should you retry vs DLQ?
5. What is the risk of DLQs?

## 15. Interview Speak

"A dead letter queue stores records that cannot be processed after validation or bounded retries. It prevents poison messages from blocking the stream while preserving the original payload and error context for investigation and replay. DLQs must be monitored and owned."

## 16. Quick Recall

- One-line summary: DLQ is quarantine for failed records.
- Three keywords: poison, retry, quarantine.
- One trap: DLQ without monitoring.
- One memory trick: Bad-address package goes to exception bin.
