# Topic 250: Fraud Detection Pipelines

## 1. Goal

Understand pipelines that detect fraud using real-time and historical signals.

## 2. Baby Intuition

Fraud detection is like a security checkpoint.

It needs to know what is happening right now and what has happened before to decide whether an action is risky.

## 3. What It Is

- Simple definition: Fraud detection pipelines score events for suspicious behavior.
- Technical definition: Fraud detection pipelines ingest transactional and behavioral events, compute real-time and historical features, apply rules/models, and produce decisions, alerts, or review queues.
- Category: Real-time risk/data pipeline.
- Related terms: risk score, rules engine, feature store, velocity feature, model serving, false positive, chargeback.

## 4. Why It Exists

Fraud changes quickly.

Signals include:

- transaction amount
- device fingerprint
- IP/location
- recent failed attempts
- account age
- merchant/user history
- velocity patterns
- known risky entities

Batch-only systems may detect fraud too late.

## 5. Where It Fits In A Data Platform

```text
transaction/login/payment event
  -> streaming feature pipeline
  -> rules/model scoring
  -> approve/deny/review decision
  -> case management and analytics lake
```

## 6. How It Works Step By Step

1. Event arrives from product system.
2. Pipeline validates/enriches event.
3. Real-time features are fetched/computed.
4. Historical features are read from feature store.
5. Rules and/or ML model produce risk score.
6. Decision is returned or alert is created.
7. Outcome labels are captured later.
8. Models/rules are retrained/tuned.

## 7. How To Use It Practically

Common features:

| Feature | Meaning |
|---|---|
| txns_last_5_min | velocity |
| failed_logins_last_10_min | suspicious account access |
| avg_amount_30d | baseline behavior |
| distance_from_last_location | impossible travel signal |
| chargebacks_90d | historical risk |

Operational needs:

- low latency
- high availability
- explainability
- false-positive monitoring
- model/rule versioning
- review workflow

## 8. Real-World Scenario

- Product/system: Credit card payment authorization.
- Problem: Decide in milliseconds whether to approve a transaction.
- How pipeline helps: real-time velocity and historical features feed a risk model/rules engine.
- What would go wrong without real-time features: rapid fraud bursts are missed.

## 9. System Design Angle

Fraud design requirements:

- decision latency
- allowed false positive rate
- model/rule explainability
- feature freshness
- fallback behavior
- audit trail
- label feedback loop

Common architecture:

```text
Kafka transaction event
  -> Flink computes velocity
  -> online feature store
  -> fraud scoring service
  -> decision + audit log
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| catches fraud quickly | false positives hurt users |
| uses real-time behavior | strict latency requirements |
| adaptive models/rules | adversaries change behavior |
| feedback loop improves model | labels may arrive late |

## 11. Failure Modes

- Failure: Feature store stale.
- Symptom: model misses current risk.
- Recovery: fallback rules or safe mode.
- Prevention: feature freshness alerts.

- Failure: Model service down.
- Symptom: cannot score transactions.
- Recovery: fallback rules/default decision.
- Prevention: HA and circuit breakers.

- Failure: Label delay.
- Symptom: model training uses late fraud outcomes.
- Recovery: delayed label pipeline.
- Prevention: label freshness tracking.

## 12. Common Mistakes

- Mistake: Optimizing only fraud catch rate.
- Why it is wrong: false positives can harm good customers.
- Better approach: balance precision, recall, business cost, and user experience.

- Mistake: No decision audit trail.
- Why it is wrong: cannot explain or debug fraud decisions.
- Better approach: log features, model/rule version, score, decision.

## 13. Mini Example

```text
Transaction:
amount=900, card_id=123

Features:
txns_last_5_min=12
avg_amount_30d=40
new_device=true

Decision:
risk_score=0.94 -> manual review/deny
```

## 14. Interview Questions

1. What data is needed for fraud detection?
2. Why do fraud systems need real-time features?
3. How do you handle model service failure?
4. What are false positives?
5. Why log decision explanations?

## 15. Interview Speak

"A fraud detection pipeline combines live events, historical features, real-time velocity features, rules, and ML scoring to make low-latency risk decisions. I would design for feature freshness, HA, fallback behavior, auditability, false-positive monitoring, and delayed label feedback."

## 16. Quick Recall

- One-line summary: Fraud pipelines score live events with real-time and historical risk signals.
- Three keywords: velocity, risk score, fallback.
- One trap: No audit trail for decisions.
- One memory trick: Security checkpoint with memory.
