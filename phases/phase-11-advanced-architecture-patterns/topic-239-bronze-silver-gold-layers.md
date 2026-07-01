# Topic 239: Bronze, Silver, Gold Layers

## 1. Goal

Understand the practical responsibilities of bronze, silver, and gold layers.

## 2. Baby Intuition

Bronze, silver, and gold are maturity levels.

Bronze is "we received it." Silver is "we cleaned it." Gold is "the business can use it."

## 3. What It Is

- Simple definition: Bronze/silver/gold are data quality and usability layers.
- Technical definition: Bronze, silver, and gold layers separate raw ingestion, cleaned/conformed data, and business-ready curated outputs in a lakehouse or warehouse pipeline.
- Category: Data platform layering.
- Related terms: medallion architecture, raw zone, curated zone, data mart, quality gates.

## 4. Why It Exists

Different users need different trust levels.

Data engineers need raw data for replay/debugging.

Analysts need clean data.

Executives need certified business metrics.

The layers prevent everyone from using the wrong maturity level.

## 5. Where It Fits In A Data Platform

```text
source systems
  -> bronze landing/raw
  -> silver cleaned/conformed
  -> gold marts/metrics
```

## 6. How It Works Step By Step

Bronze:

1. Capture source data as-is.
2. Add ingestion metadata.
3. Preserve raw history.

Silver:

1. Parse and type fields.
2. Deduplicate records.
3. Validate schemas.
4. Standardize names and formats.
5. Join or conform shared dimensions.

Gold:

1. Build facts, dimensions, aggregates, features, or metrics.
2. Apply business definitions.
3. Certify for consumers.
4. Optimize for BI/serving.

## 7. How To Use It Practically

Layer checklist:

| Layer | Common Checks |
|---|---|
| bronze | source captured, schema recorded, partitioned by ingest time |
| silver | not null keys, dedupe, type checks, bad record quarantine |
| gold | metric validation, owner, SLA, documentation, access policy |

Common pattern:

```text
bronze.order_events -> silver.orders -> gold.daily_revenue
```

## 8. Real-World Scenario

- Product/system: Subscription analytics.
- Problem: Billing events arrive with retries, duplicates, and schema changes.
- How layers help: bronze stores raw events, silver dedupes and normalizes, gold calculates MRR and churn.
- What would go wrong without layers: MRR reports depend on messy retry events.

## 9. System Design Angle

Mention these layers when:

- designing lakehouse pipelines
- explaining data quality progression
- handling raw replay/backfills
- separating engineer/analyst/business consumers

Key phrase:

```text
Each layer has a different contract.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| clear trust boundaries | extra storage |
| easier debugging | more pipelines |
| supports replay | more latency |
| cleaner business outputs | governance needed |

## 11. Failure Modes

- Failure: No quarantine for bad records.
- Symptom: silver pipeline fails or bad data leaks.
- Recovery: add quarantine/DLQ.
- Prevention: validation policy.

- Failure: Gold metric lacks owner.
- Symptom: no one resolves definition disputes.
- Recovery: assign owner/steward.
- Prevention: certified data product process.

- Failure: Bronze overwritten.
- Symptom: cannot replay original source.
- Recovery: restore backup if possible.
- Prevention: immutable raw design.

## 12. Common Mistakes

- Mistake: Naming folders bronze/silver/gold but not changing quality.
- Why it is wrong: names without contracts do not create trust.
- Better approach: define data quality and consumer rules.

- Mistake: Letting all users access all layers.
- Why it is wrong: users may consume raw sensitive data.
- Better approach: restrict bronze and promote curated data.

## 13. Mini Example

```text
Bronze:
{"orderId": "1", "amount": "10.00"}

Silver:
order_id=1, amount=10.00, valid=true

Gold:
date=2026-07-01, total_revenue=10.00
```

## 14. Interview Questions

1. Bronze vs silver vs gold?
2. Who consumes each layer?
3. Why keep bronze raw?
4. What checks belong in silver?
5. What makes gold trustworthy?

## 15. Interview Speak

"Bronze, silver, and gold layers define increasing levels of trust. Bronze captures raw replayable data, silver cleans and validates it, and gold applies business definitions for BI, ML, or product consumption."

## 16. Quick Recall

- One-line summary: Bronze is received, silver is cleaned, gold is trusted.
- Three keywords: raw, clean, business.
- One trap: Layer names without quality contracts.
- One memory trick: Data gets promoted as it matures.
