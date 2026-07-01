# Topic 233: Data Retention

## 1. Goal

Understand data retention as deciding how long data should be kept.

## 2. Baby Intuition

Data retention is like deciding how long to keep documents in a filing cabinet.

Some documents must be kept for years. Some should be deleted quickly.

## 3. What It Is

- Simple definition: Data retention defines how long data is stored before deletion, archive, or review.
- Technical definition: Data retention policies specify storage duration, archival rules, deletion schedules, legal holds, and exceptions for datasets based on business, legal, compliance, privacy, and operational needs.
- Category: Data lifecycle governance.
- Related terms: lifecycle policy, TTL, archive, deletion, legal hold, right to be forgotten, backup retention.

## 4. Why It Exists

Keeping data forever creates risk and cost:

- more storage cost
- more breach exposure
- more privacy risk
- more deletion complexity
- stale or unused datasets

But deleting too early can break:

- audits
- legal obligations
- analytics history
- model reproducibility
- recovery/backfill needs

Retention balances these needs.

## 5. Where It Fits In A Data Platform

```text
dataset created
  -> retention policy assigned
  -> lifecycle/archive/delete jobs run
  -> audit evidence retained
```

## 6. How It Works Step By Step

1. Classify dataset.
2. Identify legal/business retention needs.
3. Assign retention period.
4. Define archive/delete behavior.
5. Implement lifecycle jobs/policies.
6. Respect legal holds and exceptions.
7. Log deletion/archive actions.
8. Review policy periodically.

## 7. How To Use It Practically

Retention examples:

| Data Type | Possible Policy |
|---|---|
| raw clickstream | keep 13 months, archive after 90 days |
| debug logs | keep 30 days |
| finance records | keep per finance/legal policy |
| PII raw exports | delete quickly after use |
| backups | keep according to recovery policy |

Controls:

- object storage lifecycle rules
- table partition deletion
- snapshot expiration
- backup retention
- legal hold flags
- deletion audit logs

## 8. Real-World Scenario

- Product/system: Data lake logs.
- Problem: App logs include IP addresses and request IDs.
- How retention helps: logs are retained for operational troubleshooting for 30/90 days, then deleted or archived.
- What would go wrong without it: sensitive logs accumulate forever.

## 9. System Design Angle

Mention retention when:

- storage cost is discussed
- PII/PHI is collected
- backups and archives exist
- compliance/audit matters
- deletion workflows are needed

Key phrase:

```text
Retention should be policy-driven, not "keep everything forever."
```

## 10. Trade-offs

| Longer Retention | Shorter Retention |
|---|---|
| more history/recovery | less privacy risk |
| better audits/backfills | lower storage cost |
| model reproducibility | less breach exposure |
| more cost/risk | less historical analysis |

## 11. Failure Modes

- Failure: No retention policy.
- Symptom: data grows forever.
- Recovery: classify and define policy.
- Prevention: retention required at dataset creation.

- Failure: Deleting data under legal hold.
- Symptom: compliance/legal issue.
- Recovery: incident/legal response.
- Prevention: legal hold enforcement.

- Failure: Backups retain deleted PII indefinitely.
- Symptom: deletion incomplete.
- Recovery: align backup policy.
- Prevention: include backups in retention design.

## 12. Common Mistakes

- Mistake: Retaining raw PII because storage is cheap.
- Why it is wrong: risk grows with copies and time.
- Better approach: keep only what has purpose and policy.

- Mistake: Deleting curated data but not raw/backups.
- Why it is wrong: sensitive data remains elsewhere.
- Better approach: lineage-aware retention.

## 13. Mini Example

```text
Dataset: raw_api_logs
Retention:
  hot storage: 30 days
  archive: 180 days
  delete: after 180 days unless legal hold
```

## 14. Interview Questions

1. What is data retention?
2. Why not keep data forever?
3. How do retention and legal hold interact?
4. How do lifecycle policies help?
5. What about backups?

## 15. Interview Speak

"Data retention defines how long datasets, logs, backups, and snapshots are kept. I would classify data, assign policy based on legal/business/privacy needs, implement lifecycle/archive/delete automation, respect legal holds, and audit deletion actions."

## 16. Quick Recall

- One-line summary: Retention decides how long data lives.
- Three keywords: lifecycle, archive, delete.
- One trap: Forgetting backups and raw copies.
- One memory trick: Filing cabinet with expiration dates.
