# Topic 194: Alerting

## 1. Goal

Understand how to design useful alerts for data pipelines.

## 2. Baby Intuition

An alert is useful only if it reaches the right person at the right time with enough context to act.

A noisy alert is like an alarm that rings for burnt toast and a real fire the same way.

## 3. What It Is

- Simple definition: Alerting notifies owners when important data or pipeline problems occur.
- Technical definition: Alerting routes monitored events or threshold violations to responsible teams with severity, context, escalation, and runbook information.
- Category: Data operations and reliability.
- Related terms: alert fatigue, severity, escalation, on-call, runbook, incident, SLA.

## 4. Why It Exists

Monitoring without alerting is passive.

Alerting exists so teams can act on:

- missed SLA
- failed critical pipeline
- stale important table
- bad data quality
- schema break
- high lag
- cost spike

## 5. Where It Fits In A Data Platform

```text
monitoring detects issue
  -> alert rules classify severity
  -> alert sent to owner/channel
  -> engineer follows runbook
  -> incident closed or escalated
```

## 6. How It Works Step By Step

1. Define monitored condition.
2. Define severity and owner.
3. Add context: dataset, pipeline, time, impact, logs, lineage.
4. Send notification through Slack/email/PagerDuty/etc.
5. Escalate if not acknowledged.
6. Track resolution.
7. Tune noisy or missed alerts.

## 7. How To Use It Practically

Good alert includes:

- what broke
- when it broke
- severity
- owner
- business impact
- affected datasets/dashboards
- links to logs/runbook
- suggested first action

Bad alert:

```text
Task failed.
```

Better alert:

```text
P1: daily_revenue missed 08:00 SLA.
Impact: executive dashboard stale.
Failed task: transform_revenue.
Runbook: ...
Logs: ...
```

## 8. Real-World Scenario

- Product/system: Finance revenue dashboard.
- Problem: Critical mart misses SLA by 15 minutes.
- How alerting helps: on-call gets a high-severity alert with failed task, logs, lineage, and impact.
- What would go wrong without it: finance discovers issue during reporting meeting.

## 9. System Design Angle

Design alerting around:

- severity
- ownership
- business impact
- deduplication
- escalation
- runbooks
- quiet hours vs critical pages
- alert fatigue control

Key phrase:

```text
Every page should be actionable.
```

## 10. Trade-offs

| More Alerts | Fewer Alerts |
|---|---|
| more issues caught | less noise |
| more on-call burden | possible missed incidents |
| faster response | slower detection |
| higher sensitivity | less context switching |

## 11. Failure Modes

- Failure: Alert fatigue.
- Symptom: people ignore alerts.
- Recovery: reduce noise and tune thresholds.
- Prevention: severity and deduplication.

- Failure: No owner.
- Symptom: alert goes to dead channel.
- Recovery: assign ownership.
- Prevention: owner metadata required.

- Failure: No context.
- Symptom: slow investigation.
- Recovery: enrich alerts with logs/lineage.
- Prevention: alert template standards.

## 12. Common Mistakes

- Mistake: Paging humans for non-actionable issues.
- Why it is wrong: burns trust and attention.
- Better approach: page only urgent actionable issues.

- Mistake: Sending all alerts to one shared channel.
- Why it is wrong: ownership and accountability disappear.
- Better approach: route by dataset/pipeline owner.

## 13. Mini Example

```text
Severity:
P1: revenue dashboard stale before exec meeting
P2: important pipeline failed but has retry window
P3: non-critical table delayed
P4: informational anomaly
```

## 14. Interview Questions

1. What makes a good alert?
2. How do you avoid alert fatigue?
3. What context should alerts include?
4. How do severity levels work?
5. When should an alert page someone?

## 15. Interview Speak

"Good alerting is actionable, owned, contextual, and severity-based. I would alert on business-impacting freshness, quality, failures, lag, and SLA misses, include logs and lineage, deduplicate related alerts, and tune thresholds to avoid alert fatigue."

## 16. Quick Recall

- One-line summary: Alerting turns monitoring signals into actionable owner notifications.
- Three keywords: severity, owner, runbook.
- One trap: Noisy non-actionable alerts.
- One memory trick: Alarm should say what is burning and who handles it.
