# Topic 261: Design Fraud Detection System

## 1. Goal

Design a system that scores transactions or user actions for fraud in real time while also supporting investigation, analytics, and model improvement.

## 2. Baby Intuition

Fraud detection is a security checkpoint with memory.

It asks:

```text
is this action normal for this user,
is it risky right now,
and should we approve, deny, or review it?
```

## 3. Requirements

Clarify:

- Are we scoring payments, logins, account creation, claims, or all?
- What is the maximum decision latency?
- What is worse: false positives or false negatives?
- Do we need rules, ML, or both?
- Does the decision need to be explainable?

## 4. Functional Requirements

- ingest transaction/action events
- enrich events with user, device, merchant, IP, and history
- compute real-time velocity features
- fetch historical features from feature store
- evaluate rules and ML model
- return approve/deny/review decision
- log decision explanation and model/rule version
- collect labels such as chargebacks or confirmed fraud

## 5. Non-Functional Requirements

- low-latency scoring, often under tens or hundreds of milliseconds
- high availability
- strong auditability
- feature freshness
- safe fallback if model or feature store fails
- privacy and compliance controls
- ability to adapt as fraud patterns change

## 6. Capacity Estimation

Example:

```text
10K payment transactions/sec peak
decision latency target = 100 ms
feature lookup budget = 20-30 ms
model scoring budget = 20-40 ms
```

The exact numbers vary, but the key is showing a latency budget.

## 7. Events And APIs

Scoring API:

```text
POST /fraud/score
body: transaction/action context
response: decision, risk_score, reason_codes, model_version
```

Transaction event:

```json
{
  "transaction_id": "t1",
  "user_id": "u1",
  "amount": 900,
  "merchant_id": "m1",
  "device_id": "d1",
  "ip": "10.1.2.3",
  "event_time": "2026-07-02T10:00:00Z"
}
```

## 8. Data Model

Online feature examples:

```text
user_id -> txns_last_5_min, failed_logins_10_min, avg_amount_30d
device_id -> distinct_users_24h, risk_score
merchant_id -> chargeback_rate_30d
```

Decision log:

```text
fraud_decisions(transaction_id, user_id_hash, risk_score, decision, reason_codes, model_version, rule_version, event_time)
```

Label table:

```text
fraud_labels(transaction_id, label, label_time, source)
```

## 9. High-Level Architecture

```text
payment/login service
  -> fraud scoring API
  -> online feature store/cache
  -> rules engine + ML model
  -> approve/deny/review

transaction events
  -> Kafka
  -> stream feature computation
  -> online feature store
  -> lakehouse for training, labels, audits
```

## 10. Data Flow

1. Product service sends action to scoring API.
2. Scoring service validates request and fetches features.
3. Real-time velocity features come from online feature store.
4. Historical features come from offline/online feature pipelines.
5. Rules and ML model produce risk score and reason codes.
6. Decision is returned to product service.
7. Decision event is logged.
8. Later labels are joined with decision history for training.

## 11. Deep Dive Components

Rules engine:

- fast deterministic checks
- useful for compliance and known patterns
- easier to explain

ML model:

- catches complex patterns
- needs fresh features and labels
- requires monitoring for drift

Fallback:

- if model fails, use rules-only mode
- if feature store is stale, use conservative rules
- if scoring API is unavailable, product policy decides fail-open, fail-closed, or manual review

## 12. Scaling And Partitioning

- Partition streaming features by user_id/device_id/card_id.
- Keep online feature store horizontally scalable.
- Cache frequently used merchant/device risk features.
- Store decision logs by event_date and transaction_id.
- Use separate serving capacity for critical payment path.

## 13. Consistency And Correctness

- Real-time features should be fresh but may be eventually consistent.
- Decisions must be auditable.
- Duplicate transaction scoring should be idempotent by transaction_id.
- Feature training must be point-in-time correct.
- Labels may arrive days/weeks later, so training pipelines need delayed labels.

## 14. Failure Handling

| Failure | Handling |
|---|---|
| feature store down | fallback rules or manual review |
| model service down | rules-only mode |
| stream lag | alert on feature freshness and use degraded mode |
| duplicate request | return same decision by transaction_id |
| delayed labels | train with proper label windows |

## 15. Monitoring, Cost, And Security

Monitor:

- scoring latency
- decision distribution
- feature freshness
- model errors
- false positive/negative proxies
- review queue size
- chargeback rate

Cost:

- keep online features compact
- precompute heavy features
- archive decision logs after hot period

Security:

- encrypt sensitive transaction data
- restrict raw identifiers
- audit decision access
- store reason codes for compliance and investigation

## 16. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| rules | explainable and fast | misses complex fraud |
| ML model | catches patterns | needs monitoring and labels |
| fail-closed | safer against fraud | blocks good users |
| fail-open | protects user experience | more fraud risk |
| manual review | reduces false decisions | slower and costly |

## 17. Interview-Ready Final Answer

"I would put fraud scoring in the critical path with a strict latency budget. The product service calls a fraud API, which fetches real-time velocity and historical features from an online feature store, runs rules and an ML model, and returns approve, deny, or review with reason codes. Kafka streams transaction events into feature pipelines and the lakehouse. The lakehouse stores decisions, labels, and training data with point-in-time correctness. I would design fallbacks for model/feature failure, idempotent transaction scoring, feature freshness alerts, audit logs, and monitoring for false positives, drift, and review queue health."

## 18. Quick Recall

- One-line summary: Fraud systems make low-latency risk decisions from real-time and historical signals.
- Core tools: scoring API, rules, ML model, online feature store, Kafka, lakehouse.
- Main trap: no fallback when feature/model service fails.
- Memory trick: checkpoint with memory and reason codes.

