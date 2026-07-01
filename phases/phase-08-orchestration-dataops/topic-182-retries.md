# Topic 182: Retries

## 1. Goal

Understand retries as automatic reruns after transient task failures.

## 2. Baby Intuition

If a website times out once, you try again.

Retries do that for pipeline tasks, but with rules so they do not make things worse.

## 3. What It Is

- Simple definition: A retry reruns a failed task after a delay.
- Technical definition: Retries are configured attempts to rerun failed operations, often with delay or exponential backoff, to recover from transient errors without manual intervention.
- Category: Failure handling pattern.
- Related terms: idempotency, exponential backoff, transient failure, max attempts, retry delay.

## 4. Why It Exists

Many failures are temporary:

- network timeout
- database connection reset
- cloud API throttling
- worker lost
- temporary warehouse capacity issue
- source system unavailable for a few minutes

Retries reduce manual work and improve pipeline reliability.

## 5. Where It Fits In A Data Platform

```text
task fails
  -> wait retry delay
  -> rerun same task
  -> success or fail after max attempts
```

Retries are common in Airflow, Spark jobs, API ingestion, streaming consumers, and orchestration systems.

## 6. How It Works Step By Step

1. Task starts.
2. Task fails.
3. Orchestrator checks retry count.
4. If retries remain, task waits.
5. Task reruns.
6. If it succeeds, downstream tasks continue.
7. If retries are exhausted, task fails permanently and alerts.

## 7. How To Use It Practically

Good retry settings:

- max attempts
- delay between attempts
- exponential backoff for external systems
- timeout per attempt
- alert after final failure

Airflow-style idea:

```python
retries=3
retry_delay=timedelta(minutes=10)
retry_exponential_backoff=True
```

## 8. Real-World Scenario

- Product/system: S3 to warehouse load.
- Problem: Cloud API occasionally times out.
- How retries help: task reruns after a short delay and succeeds without human intervention.
- What would go wrong without retries: on-call gets paged for every tiny transient glitch.

## 9. System Design Angle

Retries require idempotency.

Ask:

- Is retry safe?
- Could it create duplicates?
- Is failure transient or permanent?
- Should retry use backoff?
- When should alert happen?

Rule:

```text
Retry transient errors, fail fast on deterministic bad data.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| handles transient failures | can hide real issues |
| reduces manual intervention | unsafe retries create duplicates |
| improves reliability | delays final failure signal |
| protects external systems with backoff | too many retries can amplify load |

## 11. Failure Modes

- Failure: Retrying non-idempotent task.
- Symptom: duplicate records/payments/files.
- Recovery: deduplicate/repair.
- Prevention: idempotent writes and keys.

- Failure: Retrying bad data.
- Symptom: same failure repeats and wastes time.
- Recovery: send to DLQ/quarantine and alert.
- Prevention: classify errors.

- Failure: Retry storm.
- Symptom: many tasks hammer struggling system.
- Recovery: pause/throttle.
- Prevention: exponential backoff and circuit breakers.

## 12. Common Mistakes

- Mistake: Adding retries to every task blindly.
- Why it is wrong: deterministic errors will not fix themselves.
- Better approach: retry only likely transient failures.

- Mistake: No max retry limit.
- Why it is wrong: tasks can loop forever.
- Better approach: set max attempts and alert.

## 13. Mini Example

```text
Attempt 1: warehouse connection timeout
wait 5 minutes
Attempt 2: succeeds
downstream tasks continue
```

## 14. Interview Questions

1. What are retries?
2. Why is idempotency required?
3. What is exponential backoff?
4. When should you not retry?
5. How do retries affect alerting?

## 15. Interview Speak

"Retries automatically rerun tasks after transient failures, but they are safe only when tasks are idempotent or deduplicated. I use bounded retries with delays/backoff, classify transient versus deterministic errors, and alert only after meaningful failure conditions."

## 16. Quick Recall

- One-line summary: Retries rerun transient failures safely.
- Three keywords: idempotency, backoff, max attempts.
- One trap: Retrying bad data or non-idempotent writes.
- One memory trick: Try again, but with rules.
