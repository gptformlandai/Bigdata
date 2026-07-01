# Topic 183: SLAs

## 1. Goal

Understand SLAs and freshness expectations for data pipelines.

## 2. Baby Intuition

An SLA is a promise.

For data, the promise might be: "The sales dashboard will be ready by 8 AM every business day."

## 3. What It Is

- Simple definition: An SLA defines when a pipeline or dataset must be ready.
- Technical definition: A service level agreement/objective for data pipelines defines expected availability, freshness, completion time, quality, or latency targets for data products.
- Category: Reliability and operations target.
- Related terms: SLO, freshness, deadline, alert, data product, error budget, ownership.

## 4. Why It Exists

Different data has different urgency:

- fraud signals need seconds/minutes
- executive dashboard may need 8 AM daily
- finance close may need high correctness
- ad campaign metrics may need near-real-time

SLAs make expectations explicit so teams can monitor and prioritize.

## 5. Where It Fits In A Data Platform

```text
pipeline schedule
  -> expected completion/freshness target
  -> monitor
  -> alert if missed
  -> incident response if business impact
```

## 6. How It Works Step By Step

1. Define business requirement.
2. Translate into measurable target.
3. Instrument pipeline/dataset.
4. Monitor target continuously.
5. Alert owner when target is at risk or missed.
6. Report reliability over time.
7. Improve system based on repeated misses.

Examples:

| SLA/SLO | Meaning |
|---|---|
| daily_sales ready by 07:00 | completion time |
| clickstream freshness under 10 minutes | data latency |
| null rate under 0.1% | quality |
| 99% successful hourly runs | reliability |

## 7. How To Use It Practically

For every important dataset define:

- owner
- users
- freshness target
- quality target
- alert channel
- severity rules
- business impact
- fallback/manual process

Avoid vague promises like:

```text
data should be fresh
```

Use measurable targets:

```text
orders_gold max source-to-table delay <= 30 minutes
```

## 8. Real-World Scenario

- Product/system: Daily revenue dashboard.
- Problem: Executives review revenue at 8:30 AM.
- SLA: revenue_mart must finish by 8:00 AM with validation checks passed.
- What would go wrong without SLA: failures are noticed during the meeting, not before.

## 9. System Design Angle

Mention SLAs when:

- dashboards serve business decisions
- data freshness matters
- operational dependencies exist
- alerts need severity
- trade-offs between cost and reliability appear

Maturity:

```text
Not every dataset needs the same SLA.
Critical data needs clear ownership and measurable targets.
```

## 10. Trade-offs

| Stricter SLA | Looser SLA |
|---|---|
| better freshness/reliability | lower cost |
| more monitoring/on-call | more delay tolerated |
| higher compute/engineering cost | less operational pressure |
| faster incident response | slower issue detection |

## 11. Failure Modes

- Failure: SLA not monitored.
- Symptom: missed deadline discovered by users.
- Recovery: add freshness/completion monitoring.
- Prevention: automated alerts.

- Failure: Unrealistic SLA.
- Symptom: constant pages and burnout.
- Recovery: renegotiate or improve architecture.
- Prevention: align SLA with business value.

- Failure: No owner.
- Symptom: alerts ignored.
- Recovery: assign ownership.
- Prevention: ownership metadata.

## 12. Common Mistakes

- Mistake: Giving every dataset a critical SLA.
- Why it is wrong: teams cannot treat everything as urgent.
- Better approach: classify datasets by business impact.

- Mistake: Measuring task success but not data freshness.
- Why it is wrong: pipeline may succeed with stale inputs.
- Better approach: monitor dataset freshness and quality.

## 13. Mini Example

```text
Dataset: daily_revenue
Owner: finance-data
Freshness target: by 08:00 daily
Quality target: revenue total within expected range
Alert: page if late by 15 minutes
```

## 14. Interview Questions

1. What is an SLA for data?
2. Freshness SLA vs task success?
3. How do you choose SLA severity?
4. What happens if SLA is unrealistic?
5. Why does ownership matter?

## 15. Interview Speak

"For data pipelines, SLAs should be measurable targets around freshness, completion time, quality, or availability. I would define them per critical dataset with an owner, monitor them automatically, and alert based on business impact rather than treating every pipeline failure equally."

## 16. Quick Recall

- One-line summary: SLA is the measurable reliability promise for data.
- Three keywords: freshness, owner, alert.
- One trap: Monitoring task success but not dataset freshness.
- One memory trick: Data promise with a clock.
