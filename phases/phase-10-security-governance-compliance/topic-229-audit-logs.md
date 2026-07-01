# Topic 229: Audit Logs

## 1. Goal

Understand audit logs as the evidence trail for access and changes.

## 2. Baby Intuition

Audit logs are the security camera footage of a data platform.

They tell who accessed what, when, from where, and what action happened.

## 3. What It Is

- Simple definition: Audit logs record important access and administrative actions.
- Technical definition: Audit logs are tamper-resistant records of security-relevant events such as authentication, authorization decisions, data access, policy changes, key usage, and administrative operations.
- Category: Security monitoring and compliance evidence.
- Related terms: access log, admin log, data event, SIEM, retention, immutable log, lineage.

## 4. Why It Exists

Audit logs help answer:

- who accessed this table?
- who changed this policy?
- did a job read PHI?
- when was a key used?
- what data was exported?
- what happened during an incident?

Without logs, investigations depend on guesses.

## 5. Where It Fits In A Data Platform

```text
users/jobs/admins access systems
  -> audit events emitted
  -> centralized log store/SIEM
  -> alerts, investigations, compliance reports
```

## 6. How It Works Step By Step

1. System records security-relevant event.
2. Event includes identity, action, resource, time, and result.
3. Logs are sent to central storage/monitoring.
4. Logs are protected from tampering.
5. Alerts detect suspicious patterns.
6. Logs are retained according to policy.
7. Investigators query logs during audits/incidents.

## 7. How To Use It Practically

Important events:

| Event | Example |
|---|---|
| authentication | user login, MFA failure |
| authorization | access denied/granted |
| data access | SELECT sensitive table |
| admin change | role/policy update |
| key usage | decrypt with KMS key |
| export | table unloaded to files |
| deletion | data removed/retention job |

Good practices:

- centralize logs
- protect logs from modification
- retain logs by policy
- alert on unusual access
- log service account activity
- include request IDs for tracing

## 8. Real-World Scenario

- Product/system: PHI analytics platform.
- Problem: Compliance asks who accessed a claims table last month.
- How audit logs help: logs show users/service accounts, timestamps, actions, and accessed resources.
- What would go wrong without logs: team cannot prove or investigate access.

## 9. System Design Angle

Mention audit logs when:

- sensitive data access is discussed
- compliance is relevant
- IAM policies change
- incident response is needed
- deletion/right-to-be-forgotten workflows exist

Key phrase:

```text
If access matters, log it and protect the log.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| supports investigations | log storage cost |
| compliance evidence | privacy of logs matters |
| detects suspicious activity | noisy signals need tuning |
| accountability | logs must be protected |

## 11. Failure Modes

- Failure: Logs disabled.
- Symptom: no evidence during incident.
- Recovery: enable and document gap.
- Prevention: audit-by-default.

- Failure: Logs mutable by admins being audited.
- Symptom: tampering risk.
- Recovery: move to protected store.
- Prevention: immutable/append-only controls.

- Failure: Logs contain sensitive data.
- Symptom: logs become another PII/PHI store.
- Recovery: scrub and restrict.
- Prevention: avoid logging payloads/secrets.

## 12. Common Mistakes

- Mistake: Logging only pipeline success/failure.
- Why it is wrong: security investigations need access and admin events.
- Better approach: capture data, policy, auth, and key events.

- Mistake: Letting logs expire too soon.
- Why it is wrong: audits/incidents may need historical evidence.
- Better approach: retention by compliance and business policy.

## 13. Mini Example

```text
timestamp=2026-07-02T10:15:00Z
principal=analyst_123
action=SELECT
resource=warehouse.raw_claims_phi
result=DENY
reason=missing_phi_reader_role
```

## 14. Interview Questions

1. What are audit logs?
2. What events should be logged?
3. Why protect audit logs?
4. How do audit logs help compliance?
5. What is risky about logging payloads?

## 15. Interview Speak

"Audit logs are the evidence trail for data access, authentication, policy changes, key usage, exports, and administrative actions. I would centralize and protect logs, retain them by policy, alert on suspicious activity, and avoid logging sensitive payloads."

## 16. Quick Recall

- One-line summary: Audit logs record who did what, when, and where.
- Three keywords: identity, action, evidence.
- One trap: Logs that contain sensitive data or can be modified.
- One memory trick: Security camera for the data platform.
