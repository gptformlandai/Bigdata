# Topic 255: Data Platform Reliability

## 1. Goal

Understand how to make data platforms dependable under failures, delays, bad data, and scale.

## 2. Baby Intuition

Data platform reliability means people can trust the data to arrive, be correct enough, and be usable on time.

It is not only "the server is up." It is also "the dashboard is fresh, complete, and not lying."

## 3. What It Is

- Simple definition: Data platform reliability keeps data systems trustworthy and available.
- Technical definition: Data platform reliability is the practice of designing, monitoring, and operating ingestion, processing, storage, serving, and governance systems to meet freshness, correctness, completeness, availability, and latency expectations.
- Category: DataOps/platform engineering discipline.
- Related terms: SLI, SLO, SLA, freshness, completeness, correctness, observability, incident response, replay, idempotency.

## 4. Why It Exists

Data failures can be silent.

A service outage is obvious. A data issue may look normal while business decisions are wrong.

Examples:

- dashboard is missing yesterday's revenue
- fraud model uses stale features
- CDC missed delete events
- streaming job is running but lagging
- warehouse table is duplicated
- schema change breaks a downstream report

## 5. Where It Fits In A Data Platform

```text
sources
  -> ingestion reliability
  -> processing reliability
  -> storage/table reliability
  -> serving reliability
  -> monitoring, alerting, incident response
```

Reliability is not one tool. It is built into every layer.

## 6. How It Works Step By Step

1. Define what reliable means for each dataset or pipeline.
2. Choose SLIs such as freshness, completeness, error rate, and latency.
3. Set SLOs with owners and severity.
4. Build idempotent pipelines so retries are safe.
5. Add checkpoints, replay, DLQs, and backfills.
6. Validate schemas and data quality.
7. Monitor pipeline health and data health.
8. Alert on user-impacting issues.
9. Run incident response and postmortems.
10. Improve prevention after every major issue.

## 7. How To Use It Practically

Core reliability signals:

| Signal | Question |
|---|---|
| freshness | is data updated on time? |
| completeness | did all expected records arrive? |
| correctness | does data pass quality rules? |
| latency | how long from event to serving? |
| availability | can users query it? |
| cost/resource health | is the platform sustainable? |

Common mechanisms:

- idempotent writes
- retries with backoff
- checkpointing
- dead letter queues
- schema contracts
- data quality checks
- lineage
- backfills
- replayable streams
- runbooks

## 8. Real-World Scenario

- Product/system: Executive revenue dashboard.
- Problem: Leaders need daily revenue by 8 AM.
- How reliability helps: pipeline has freshness SLO, completeness checks, source arrival checks, alerting, runbook, and backfill procedure.
- What would go wrong without it: dashboard may show incomplete revenue and nobody notices until decisions are made.

## 9. System Design Angle

For any MAANG data design, mention reliability explicitly:

- What happens if the source is late?
- Can the pipeline replay data?
- Are writes idempotent?
- How are duplicates handled?
- How are schema changes handled?
- How do we detect stale or incorrect data?
- Who owns the dataset?
- What is the fallback during incidents?

Strong interview line:

```text
I would monitor both pipeline health and data health.
```

Pipeline health means jobs are running.
Data health means the output is fresh, complete, and valid.

## 10. Trade-offs

| Pros | Cons |
|---|---|
| higher trust in data | more engineering effort |
| faster incident detection | monitoring cost |
| safer retries/replays | more metadata needed |
| better interview/system maturity | requires ownership discipline |

## 11. Failure Modes

- Failure: Silent data corruption.
- Symptom: pipeline succeeds but values are wrong.
- Recovery: stop downstream publishing and backfill corrected data.
- Prevention: quality checks and anomaly detection.

- Failure: Duplicate processing.
- Symptom: counts/revenue inflated.
- Recovery: deduplicate and recompute.
- Prevention: idempotent sinks and primary keys.

- Failure: Source delay.
- Symptom: dashboard stale or partial.
- Recovery: mark data delayed and rerun when source arrives.
- Prevention: source freshness monitoring.

- Failure: Schema drift.
- Symptom: downstream parser/query fails.
- Recovery: update contract and transform.
- Prevention: schema registry and compatibility checks.

## 12. Common Mistakes

- Mistake: Alerting only when a job fails.
- Why it is wrong: job can succeed with bad or incomplete data.
- Better approach: monitor freshness, completeness, correctness, and business metrics.

- Mistake: Retrying non-idempotent writes.
- Why it is wrong: retries can duplicate records.
- Better approach: design upserts, merge keys, dedupe keys, or transactional commits.

## 13. Mini Example

```text
Dataset: gold.daily_revenue
SLO: available by 08:00 with 99% monthly success

Checks:
- source_orders_arrived = true
- row_count within expected range
- revenue not negative
- freshness under 24 hours
```

## 14. Interview Questions

1. What does reliability mean for data platforms?
2. Pipeline health vs data health?
3. How do you make retries safe?
4. How do you detect stale data?
5. What is your incident response plan for bad data?

## 15. Interview Speak

"For data platform reliability, I would define SLIs and SLOs around freshness, completeness, correctness, latency, and availability. Then I would build idempotent pipelines with checkpoints, retries, DLQs, replay/backfill support, schema contracts, data quality checks, monitoring, alerting, runbooks, and postmortems."

## 16. Quick Recall

- One-line summary: Data reliability means fresh, complete, valid, available data.
- Three keywords: freshness, idempotency, observability.
- One trap: monitoring only job success.
- One memory trick: The dashboard must be up and truthful.

