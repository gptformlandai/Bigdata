# Phase 11: Advanced Architecture Patterns

Phase 11 teaches the architecture patterns that appear again and again in MAANG-level Big Data system design.

The mental model is:

```text
data platforms are built from repeatable patterns
  -> ingestion patterns
  -> batch/stream processing patterns
  -> serving patterns
  -> reliability patterns
  -> domain-specific pipelines
```

This phase connects the tools from earlier phases into real architecture shapes.

## Topics

| # | Topic | Status |
|---:|---|---|
| 236 | Lambda architecture | Complete |
| 237 | Kappa architecture | Complete |
| 238 | Medallion architecture | Complete |
| 239 | Bronze, silver, gold layers | Complete |
| 240 | CDC | Complete |
| 241 | Debezium | Complete |
| 242 | Outbox pattern | Complete |
| 243 | Saga pattern | Complete |
| 244 | Event sourcing | Complete |
| 245 | CQRS | Complete |
| 246 | Feature stores | Complete |
| 247 | Real-time feature pipelines | Complete |
| 248 | Search analytics pipelines | Complete |
| 249 | Recommendation data pipelines | Complete |
| 250 | Fraud detection pipelines | Complete |
| 251 | Metrics platform | Complete |
| 252 | Logging platform | Complete |
| 253 | Time-series analytics | Complete |
| 254 | Multi-tenant data platforms | Complete |
| 255 | Data platform reliability | Complete |

## Phase Goal

By the end of this phase, you should be able to explain:

- why Lambda and Kappa architectures exist
- how medallion layers organize lakehouse data
- how CDC, Debezium, and Outbox move database changes safely
- why Saga, Event Sourcing, and CQRS matter in distributed systems
- how feature stores and real-time feature pipelines support ML
- how search, recommendation, fraud, metrics, logging, and time-series pipelines are designed
- how multi-tenant and reliable data platforms are operated at scale

## Suggested Study Flow

1. Read Topics 236-239 for high-level platform architecture shapes.
2. Read Topics 240-245 for event and consistency patterns.
3. Read Topics 246-250 for ML/search/fraud data pipelines.
4. Read Topics 251-255 for platform reliability and operational architectures.
5. Finish with `phase-11-review.md`.

## Examples

Run these small programs after the related topic:

| Example | Related Topic | What It Shows |
|---|---:|---|
| `examples/topic_240_cdc_apply_changes_demo.py` | 240 | applying insert/update/delete CDC events |
| `examples/topic_242_outbox_relay_demo.py` | 242 | outbox relay and duplicate-safe publishing |
| `examples/topic_246_feature_store_point_in_time_demo.py` | 246 | point-in-time feature lookup |
| `examples/topic_251_metrics_rollup_demo.py` | 251 | rolling request events into metrics |
