# Topic 202: AWS Lambda For Data

## 1. Goal

Understand how AWS Lambda can be used in data pipelines without misusing it for heavy processing.

## 2. Baby Intuition

Lambda is like a tiny worker that wakes up when an event happens, does a small job, and goes back to sleep.

It is great for glue logic, not for processing terabytes.

## 3. What It Is

- Simple definition: Lambda runs small serverless functions triggered by events.
- Technical definition: AWS Lambda is a serverless compute service that executes function code in response to triggers such as S3 events, streams, schedules, API calls, or messages.
- Category: Serverless event-driven compute.
- Related terms: trigger, event, function, timeout, idempotency, S3 event, Kinesis consumer, DLQ.

## 4. Why It Exists

Some pipeline work is small and event-driven:

- validate a file arrival
- start a Glue job
- route a message
- transform a small event
- write metadata
- send notification
- update a catalog entry

Lambda exists so teams do not need to run servers for small event-triggered tasks.

## 5. Where It Fits In A Data Platform

```text
S3 event / Kinesis record / schedule / API
  -> Lambda function
  -> trigger ETL, validate metadata, route event, notify, or write small output
```

Lambda often coordinates or reacts; heavy compute should go to Glue, EMR, Spark, warehouses, or streaming processors.

## 6. How It Works Step By Step

1. Event occurs.
2. Lambda service invokes function.
3. Function receives event payload.
4. Function performs bounded work.
5. Function writes output or calls another service.
6. Success/failure is recorded.
7. Retries/DLQ/error handling depend on trigger type and configuration.

## 7. How To Use It Practically

Good data use cases:

- S3 file arrival validation
- start Glue workflow
- lightweight metadata extraction
- small JSON transformation
- stream record enrichment for low volume
- alert notification

Avoid:

- large Spark-like transforms
- long-running jobs
- huge file processing
- stateful stream processing
- heavy joins

## 8. Real-World Scenario

- Product/system: New file ingestion trigger.
- Problem: When a partner uploads a file to S3, the pipeline should validate naming and start ETL.
- How Lambda helps: S3 event triggers Lambda; Lambda checks file path and starts Glue/Airflow workflow.
- What would go wrong if misused: trying to process the full large file inside Lambda hits limits and becomes brittle.

## 9. System Design Angle

Use Lambda for:

- event triggers
- lightweight orchestration glue
- small transformations
- notifications
- metadata operations

Do not use Lambda as:

- Spark replacement
- warehouse replacement
- long-running batch compute

Key phrase:

```text
Lambda is great for event glue, not big data crunching.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| serverless and event-driven | runtime/time/resource limits |
| no server management | cold starts can matter |
| integrates with AWS events | retries require idempotency |
| good for small glue logic | not for TB-scale processing |

## 11. Failure Modes

- Failure: Non-idempotent retry.
- Symptom: duplicate downstream actions.
- Recovery: dedupe and repair.
- Prevention: idempotency keys.

- Failure: Large file processed in function.
- Symptom: timeout/memory failure.
- Recovery: move processing to Glue/EMR.
- Prevention: use Lambda only to trigger heavy job.

- Failure: Missing permissions.
- Symptom: function cannot read S3/start job.
- Recovery: fix IAM role.
- Prevention: least-privilege policy tests.

## 12. Common Mistakes

- Mistake: Using Lambda for heavy ETL.
- Why it is wrong: Lambda is bounded serverless compute, not distributed data processing.
- Better approach: Lambda triggers Glue/EMR/Dataflow/Spark.

- Mistake: Ignoring duplicate events.
- Why it is wrong: event-driven systems may retry.
- Better approach: make handlers idempotent.

## 13. Mini Example

```text
S3 object created:
s3://partner-feed/orders/2026-07-01.csv

Lambda:
validate path
record metadata
start Glue job
notify on failure
```

## 14. Interview Questions

1. What is Lambda?
2. How can Lambda be used in data pipelines?
3. Why not process huge files in Lambda?
4. What is idempotency for Lambda?
5. Lambda vs Glue/EMR?

## 15. Interview Speak

"Lambda is useful for serverless event-driven glue in data platforms: reacting to file arrivals, triggering jobs, validating metadata, routing events, and sending notifications. I would not use it for heavy batch processing; it should trigger scalable compute like Glue, EMR, Spark, or warehouse jobs."

## 16. Quick Recall

- One-line summary: Lambda is small event-driven compute for data glue logic.
- Three keywords: trigger, serverless, idempotency.
- One trap: Using Lambda as a Spark replacement.
- One memory trick: Tiny worker wakes on event.
