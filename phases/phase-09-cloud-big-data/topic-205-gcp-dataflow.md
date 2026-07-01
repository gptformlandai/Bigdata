# Topic 205: GCP Dataflow

## 1. Goal

Understand Dataflow as GCP's managed service for Apache Beam batch and streaming pipelines.

## 2. Baby Intuition

Dataflow is like a managed conveyor belt for data.

It can process bounded files or continuous streams using the same Beam programming model.

## 3. What It Is

- Simple definition: Dataflow is managed stream and batch processing on GCP.
- Technical definition: Google Cloud Dataflow runs Apache Beam pipelines as a managed service for batch and streaming data processing, autoscaling workers and integrating with GCP sources/sinks.
- Category: Managed data processing / stream processing.
- Related terms: Apache Beam, pipeline, PCollection, windowing, Pub/Sub, Cloud Storage, BigQuery, autoscaling.

## 4. Why It Exists

Data teams need to process:

- streaming events
- files in object storage
- windowed aggregations
- ETL transformations
- Pub/Sub messages
- BigQuery loads

Dataflow exists to run these pipelines without managing worker clusters directly.

## 5. Where It Fits In A Data Platform

```text
Pub/Sub or Cloud Storage
  -> Dataflow Beam pipeline
  -> BigQuery / Cloud Storage / other sinks
```

It is commonly used for streaming ETL on GCP.

## 6. How It Works Step By Step

1. Developer writes Apache Beam pipeline.
2. Pipeline defines input, transforms, windows/triggers if streaming, and output.
3. Submit pipeline to Dataflow.
4. Dataflow provisions and scales workers.
5. Workers process records in parallel.
6. Output is written to BigQuery, Cloud Storage, Pub/Sub, etc.
7. Monitoring tracks throughput, lag, errors, and worker health.

## 7. How To Use It Practically

Common patterns:

| Pattern | Example |
|---|---|
| streaming ETL | Pub/Sub events to BigQuery |
| batch ETL | Cloud Storage files to curated output |
| windowed metrics | 5-minute event counts |
| data enrichment | join event with reference data |
| file conversion | JSON/CSV to Parquet |

Important design:

- event time vs processing time
- windows and late data
- dead-letter paths
- idempotent sinks
- monitoring lag/freshness

## 8. Real-World Scenario

- Product/system: Real-time app analytics.
- Problem: User events arrive in Pub/Sub and need cleaning plus BigQuery insertion within minutes.
- How Dataflow helps: Beam streaming pipeline parses, validates, windows, and writes to BigQuery.
- What would go wrong without DLQ: poison records can repeatedly fail processing.

## 9. System Design Angle

Use Dataflow when:

- GCP-managed streaming/batch processing is needed
- Pub/Sub and BigQuery integration matters
- Apache Beam model fits
- autoscaling stream processing is useful

Consider Dataproc when:

- Spark ecosystem/control is preferred

Consider BigQuery SQL when:

- transformation is warehouse-only SQL

## 10. Trade-offs

| Pros | Cons |
|---|---|
| managed Beam execution | Beam learning curve |
| supports batch and streaming | debugging distributed pipelines can be hard |
| autoscaling | pipeline design affects cost |
| strong GCP integration | not ideal for every Spark workload |

## 11. Failure Modes

- Failure: Bad messages.
- Symptom: pipeline errors/retries.
- Recovery: DLQ/quarantine.
- Prevention: schema validation.

- Failure: Lag grows.
- Symptom: outputs stale.
- Recovery: scale/tune pipeline.
- Prevention: lag alerts.

- Failure: Sink bottleneck.
- Symptom: writes slow/fail.
- Recovery: tune batching/sink config.
- Prevention: capacity planning.

## 12. Common Mistakes

- Mistake: Ignoring event time and late data.
- Why it is wrong: streaming metrics become wrong.
- Better approach: design windows/watermarks/late data policy.

- Mistake: No dead-letter path.
- Why it is wrong: bad records can block or hide failures.
- Better approach: route invalid records for inspection.

## 13. Mini Example

```text
Pub/Sub clicks
  -> Dataflow parses and validates
  -> 1-minute window aggregation
  -> BigQuery realtime table
  -> dashboard
```

## 14. Interview Questions

1. What is Dataflow?
2. What is Apache Beam?
3. Dataflow vs Dataproc?
4. How do you handle late events?
5. How do you monitor streaming lag?

## 15. Interview Speak

"Dataflow is GCP's managed Apache Beam service for batch and streaming pipelines. I would use it for Pub/Sub-to-BigQuery streaming ETL, windowed aggregations, and managed scaling, with careful design around event time, late data, DLQs, idempotent sinks, and lag monitoring."

## 16. Quick Recall

- One-line summary: Dataflow runs managed Beam batch/stream pipelines.
- Three keywords: Beam, Pub/Sub, windowing.
- One trap: Ignoring late events.
- One memory trick: Managed data conveyor belt.
