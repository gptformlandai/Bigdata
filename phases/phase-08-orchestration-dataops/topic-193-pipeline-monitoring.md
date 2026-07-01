# Topic 193: Pipeline Monitoring

## 1. Goal

Understand what to monitor in production data pipelines.

## 2. Baby Intuition

Pipeline monitoring is like watching a factory line.

You need to know if the machines are running, outputs are complete, quality is good, and delivery is on time.

## 3. What It Is

- Simple definition: Pipeline monitoring tracks whether data pipelines are running correctly.
- Technical definition: Pipeline monitoring collects operational and data health signals such as task state, duration, retries, failures, freshness, volume, quality, lag, resource usage, and SLA status.
- Category: Data operations.
- Related terms: task status, freshness, lag, SLA, error rate, duration, logs, metrics.

## 4. Why It Exists

Pipelines fail in many ways:

- task fails
- task hangs
- task succeeds late
- task succeeds with stale input
- row count drops
- data quality check fails
- streaming lag grows
- cost spikes

Monitoring lets teams detect and act.

## 5. Where It Fits In A Data Platform

```text
orchestrator + compute engines + warehouse/lake + quality checks
  -> metrics/logs/events
  -> monitoring dashboard
  -> alerts and runbooks
```

## 6. How It Works Step By Step

1. Define important pipelines and datasets.
2. Collect task-level metrics.
3. Collect data-level metrics.
4. Collect resource/cost metrics.
5. Compare against thresholds/SLOs.
6. Alert owners when important thresholds break.
7. Use logs/lineage to investigate.
8. Improve based on repeated incidents.

## 7. How To Use It Practically

Monitor:

| Signal | Example |
|---|---|
| task state | success/failure/queued/running |
| duration | task took 3x normal |
| retries | repeated transient failures |
| freshness | table is 2 hours stale |
| volume | rows dropped 80% |
| quality | null check failed |
| lag | Kafka/Flink consumer lag |
| cost | query or job cost spike |

## 8. Real-World Scenario

- Product/system: Hourly fraud features pipeline.
- Problem: Streaming lag grows and features become stale.
- How monitoring helps: lag/freshness alerts tell the team before fraud model quality degrades.
- What would go wrong without it: product keeps using stale features silently.

## 9. System Design Angle

Pipeline monitoring should cover:

- orchestration health
- compute job health
- data freshness
- data quality
- dependency health
- cost/resource usage
- business SLA

Important:

```text
Monitor outcomes, not only task mechanics.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| catches failures early | setup effort |
| improves reliability | alert tuning required |
| helps capacity planning | can produce noise |
| supports SLA reporting | metrics storage cost |

## 11. Failure Modes

- Failure: Monitoring only Airflow failures.
- Symptom: stale data task succeeds.
- Recovery: add dataset freshness checks.
- Prevention: monitor data outcomes.

- Failure: No duration monitoring.
- Symptom: pipeline slowly degrades until SLA miss.
- Recovery: add duration thresholds.
- Prevention: baseline normal runtime.

- Failure: Logs not retained.
- Symptom: incident hard to debug.
- Recovery: improve log retention.
- Prevention: centralized logging.

## 12. Common Mistakes

- Mistake: Alerting on every task failure equally.
- Why it is wrong: not all failures have equal business impact.
- Better approach: severity by dataset/product criticality.

- Mistake: No monitoring for upstream dependencies.
- Why it is wrong: source delays cause downstream failures.
- Better approach: monitor inputs and outputs.

## 13. Mini Example

```text
Pipeline: daily_sales
task success: yes
duration: under 30 min
freshness: table updated by 07:30
quality: revenue >= 0, order_id unique
SLA: dashboard ready by 08:00
```

## 14. Interview Questions

1. What do you monitor in pipelines?
2. Task monitoring vs data monitoring?
3. How do you detect stale data?
4. What metrics show pipeline degradation?
5. How do you reduce noisy alerts?

## 15. Interview Speak

"Pipeline monitoring should include task state, runtime, retries, logs, freshness, volume, quality checks, lag, resource usage, and SLA status. I care about data outcomes, not only whether a task exited successfully."

## 16. Quick Recall

- One-line summary: Pipeline monitoring watches tasks, data, and SLAs.
- Three keywords: state, freshness, quality.
- One trap: Monitoring only job success.
- One memory trick: Factory line plus product inspection.
