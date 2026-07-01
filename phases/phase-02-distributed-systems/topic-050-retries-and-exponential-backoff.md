# Topic 050: Retries And Exponential Backoff

## Goal

Understand how retries recover from temporary failures and why backoff is necessary to avoid overload.

## Simple Explanation

Retries try again after failure.

Exponential backoff waits longer between each retry:

```text
1s -> 2s -> 4s -> 8s
```

## Core Idea

- Definition: Retry is repeating a failed operation; exponential backoff increases wait time after each failure.
- Why it matters: Many failures are temporary, but immediate repeated retries can overload systems.
- Related terms: timeout, jitter, retry budget, idempotency, circuit breaker.

## When To Retry

Usually retry:

- timeouts
- `429 Too Many Requests`
- `500/502/503/504`
- temporary network errors
- leader failover errors

Usually do not retry blindly:

- `400 Bad Request`
- `401 Unauthorized`
- validation failures
- permission errors
- non-idempotent operations without protection

## How It Works

Basic retry flow:

1. Send request.
2. If it succeeds, return.
3. If it fails with retryable error, wait.
4. Increase delay.
5. Add jitter.
6. Stop after max attempts or deadline.

Jitter means adding randomness so all clients do not retry at the same moment.

## Big Data / System Design Angle

Retries appear in:

- API ingestion
- Kafka producers
- database writes
- Airflow tasks
- Spark task failures
- object storage calls
- CDC connectors

Retry risks:

- duplicate writes
- retry storms
- delayed pipelines
- hidden dependency outage
- overload amplification

Safe retry checklist:

- timeout
- max attempts
- exponential backoff
- jitter
- idempotency
- observability
- dead letter path for permanent failure

## Example

```python
import random
import time


def retry_delay(attempt, base=1.0, cap=30.0):
    delay = min(cap, base * (2 ** attempt))
    jitter = random.uniform(0, delay * 0.2)
    return delay + jitter


for attempt in range(5):
    print(f"attempt={attempt + 1}, wait={retry_delay(attempt):.2f}s")
```

## Common Mistakes

- Mistake: Infinite retries.
- Better way: Use max attempts and deadlines.

- Mistake: Retrying without jitter.
- Better way: Add jitter to avoid synchronized retry spikes.

- Mistake: Retrying non-idempotent writes.
- Better way: add idempotency keys or avoid retrying unsafe operations.

## Interview Speak

"Retries handle transient failures, but I would use exponential backoff, jitter, timeouts, max attempts, and idempotency. Otherwise retries can create duplicate writes or amplify an outage into a retry storm."

## Quick Recall

- One-liner: Retry temporary failures, but back off and make them safe.
- Keywords: backoff, jitter, idempotency.
- Trap: Infinite retries during an outage.
