# Topic 195: Incident Response For Data Pipelines

## 1. Goal

Understand how teams respond when production data pipelines break or produce bad data.

## 2. Baby Intuition

Incident response is the emergency plan.

When data is late or wrong, the team needs roles, steps, communication, recovery, and learning.

## 3. What It Is

- Simple definition: Incident response is the process for handling production data problems.
- Technical definition: Data pipeline incident response is a structured operational workflow for detecting, triaging, mitigating, communicating, resolving, and learning from data reliability incidents.
- Category: Data reliability operations.
- Related terms: severity, on-call, runbook, root cause analysis, postmortem, mitigation, rollback.

## 4. Why It Exists

Data incidents can affect:

- executive decisions
- customer-facing dashboards
- ML models
- billing
- fraud detection
- finance reporting
- compliance

Without a response process, teams waste time deciding what to do during the outage.

## 5. Where It Fits In A Data Platform

```text
monitoring/alerting detects issue
  -> triage severity and impact
  -> mitigate
  -> fix/recover
  -> communicate
  -> postmortem and prevention
```

## 6. How It Works Step By Step

1. Alert or user report arrives.
2. Acknowledge incident.
3. Identify severity and impacted users/data products.
4. Stop further damage if needed.
5. Find root cause or immediate cause.
6. Mitigate: rollback, pause, rerun, backfill, or quarantine.
7. Validate recovered data.
8. Communicate status and resolution.
9. Write postmortem for significant incidents.
10. Add prevention actions.

## 7. How To Use It Practically

Incident runbook should include:

- owner/on-call
- severity definitions
- first checks
- dashboards/log links
- rollback steps
- backfill steps
- communication template
- escalation contacts
- validation checklist

Common mitigations:

| Problem | Mitigation |
|---|---|
| bad deploy | rollback/revert |
| stale source | communicate delay/fallback |
| bad data published | quarantine table or restore previous version |
| failed partition | rerun/backfill |
| duplicate data | dedupe and repair |

## 8. Real-World Scenario

- Product/system: Fraud feature pipeline.
- Problem: Feature table stops updating and model uses stale features.
- Response: alert triggers, team identifies failed upstream stream job, switches model to fallback features or pauses scoring, fixes job, validates freshness, and documents prevention.
- What would go wrong without response process: stale features silently harm fraud decisions.

## 9. System Design Angle

Strong systems include:

- detection
- ownership
- severity
- runbooks
- rollback/time travel
- raw replay/backfill
- communication
- postmortems

Key phrase:

```text
Recovery design is part of pipeline design.
```

## 10. Trade-offs

| Fast Mitigation | Perfect Fix |
|---|---|
| reduces business impact | may be temporary |
| quicker communication | root cause still needed |
| can use rollback/fallback | may require later cleanup |
| protects users | long-term prevention comes after |

## 11. Failure Modes

- Failure: No owner.
- Symptom: nobody acts.
- Recovery: assign incident commander/owner.
- Prevention: ownership metadata.

- Failure: No rollback/backfill path.
- Symptom: recovery takes too long.
- Recovery: rebuild manually.
- Prevention: design replay and versioning.

- Failure: Poor communication.
- Symptom: users distrust data.
- Recovery: status updates and final summary.
- Prevention: incident communication templates.

## 12. Common Mistakes

- Mistake: Only fixing the immediate failed task.
- Why it is wrong: downstream data may remain wrong.
- Better approach: validate and repair all impacted datasets.

- Mistake: Skipping postmortem.
- Why it is wrong: repeated incidents continue.
- Better approach: document root cause and prevention actions.

## 13. Mini Example

```text
Incident:
daily_revenue is wrong after bad discount logic deploy

Mitigation:
rollback dbt model
restore previous table version
backfill affected dates
validate totals
notify finance and dashboard owners
write postmortem
```

## 14. Interview Questions

1. How do you respond to a failed critical pipeline?
2. What is the first step after an alert?
3. How do you assess impact?
4. How do rollback and backfill help?
5. What should a postmortem include?

## 15. Interview Speak

"For a data incident, I would acknowledge the alert, assess severity and downstream impact, stop further damage, mitigate with rollback/quarantine/fallback if needed, fix or rerun/backfill, validate outputs, communicate with stakeholders, and write a postmortem with prevention actions."

## 16. Quick Recall

- One-line summary: Incident response is the playbook for late or wrong production data.
- Three keywords: impact, mitigation, postmortem.
- One trap: Fixing the task but not repairing downstream data.
- One memory trick: Detect, contain, repair, learn.
