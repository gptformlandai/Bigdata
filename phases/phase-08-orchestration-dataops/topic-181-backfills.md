# Topic 181: Backfills

## 1. Goal

Understand backfills as rerunning pipelines for past dates or historical data ranges.

## 2. Baby Intuition

A backfill is filling missing pages in an old notebook.

If a pipeline was broken last week, you rerun those old days to repair history.

## 3. What It Is

- Simple definition: A backfill reruns a data pipeline for past time periods.
- Technical definition: A backfill reprocesses historical partitions, dates, or data intervals to populate missing outputs, repair incorrect data, or apply new logic to old data.
- Category: Data pipeline recovery and historical processing.
- Related terms: catchup, partition, rerun, idempotency, replay, historical load.

## 4. Why It Exists

Backfills are needed when:

- a pipeline failed for past dates
- business logic changed
- a new table is created from historical data
- bad data needs correction
- source system replay is required
- late-arriving data must be incorporated

Without backfills, history stays incomplete or wrong.

## 5. Where It Fits In A Data Platform

```text
historical input partitions
  -> rerun pipeline logic
  -> historical output partitions repaired/rebuilt
```

Backfills are common in Airflow, Spark, dbt, lakehouse, and warehouse pipelines.

## 6. How It Works Step By Step

1. Identify affected date/data range.
2. Confirm source data exists.
3. Ensure tasks are idempotent.
4. Pause or coordinate with regular schedule if needed.
5. Run historical pipeline instances.
6. Validate outputs.
7. Recompute downstream aggregates.
8. Monitor cost and system load.

## 7. How To Use It Practically

Good backfill checklist:

- define start/end dates
- estimate data volume
- choose parallelism limit
- avoid overwriting good data accidentally
- validate counts and quality
- communicate dashboard impact
- track completion

Example:

```text
Backfill orders from 2026-06-01 to 2026-06-30 after fixing tax logic.
```

## 8. Real-World Scenario

- Product/system: Revenue warehouse.
- Problem: Discount calculation was wrong for 15 days.
- How backfill helps: rerun affected partitions and downstream revenue marts with corrected logic.
- What would go wrong without it: historical reports remain wrong.

## 9. System Design Angle

Mention backfills when:

- historical correctness matters
- pipeline logic changes
- late data arrives
- replay from raw lake/Kafka/source exists
- data must be reproducible

Key design:

```text
Keep immutable raw data so curated tables can be rebuilt.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| repairs history | can be expensive |
| supports new logic | may overload systems |
| improves trust | needs idempotent tasks |
| enables reproducibility | downstream recomputation required |

## 11. Failure Modes

- Failure: Non-idempotent backfill.
- Symptom: duplicate data.
- Recovery: clean outputs and rerun safely.
- Prevention: overwrite/merge by partition/key.

- Failure: Backfill overloads warehouse/source.
- Symptom: production jobs slow.
- Recovery: throttle parallelism.
- Prevention: capacity plan and schedule off-hours.

- Failure: Downstream not backfilled.
- Symptom: upstream fixed but dashboard still wrong.
- Recovery: rerun dependent models.
- Prevention: dependency-aware backfill plan.

## 12. Common Mistakes

- Mistake: Backfilling without validation.
- Why it is wrong: you may replace bad data with different bad data.
- Better approach: compare counts, totals, nulls, and samples.

- Mistake: Assuming current code can always process old data.
- Why it is wrong: schemas and source meanings may have changed.
- Better approach: check historical schema compatibility.

## 13. Mini Example

```text
Bad partition:
orders/dt=2026-06-15

Backfill:
delete/overwrite partition
rerun transform for 2026-06-15
validate row count and revenue total
```

## 14. Interview Questions

1. What is a backfill?
2. Why is idempotency important?
3. How do you backfill safely?
4. What is catchup?
5. How do backfills affect downstream tables?

## 15. Interview Speak

"A backfill reruns pipeline logic for historical data ranges to repair or rebuild outputs. I plan backfills by date range, source availability, idempotency, downstream dependencies, validation checks, and resource limits so historical correction does not damage production."

## 16. Quick Recall

- One-line summary: Backfill reruns the past safely.
- Three keywords: history, idempotency, validation.
- One trap: Creating duplicates during rerun.
- One memory trick: Fill missing old notebook pages.
