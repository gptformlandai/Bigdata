# Topic 188: Data Pipeline Testing

## 1. Goal

Understand how to test data pipelines for code correctness and data correctness.

## 2. Baby Intuition

Testing a pipeline is like checking both the machine and the product it produces.

The code can run successfully but still produce wrong data.

## 3. What It Is

- Simple definition: Data pipeline testing verifies pipeline code and output data.
- Technical definition: Data pipeline testing includes unit, integration, schema, data quality, regression, freshness, and end-to-end checks that validate pipeline behavior and produced datasets.
- Category: Data quality and software testing.
- Related terms: unit test, integration test, schema test, data quality test, regression test, row count, freshness.

## 4. Why It Exists

Pipelines can fail silently:

- wrong join duplicates rows
- nulls appear in key columns
- schema changes break assumptions
- late data creates missing partitions
- metric logic changes unexpectedly
- task succeeds but output is incomplete

Testing catches these before users do.

## 5. Where It Fits In A Data Platform

```text
development
  -> CI tests
  -> pipeline run tests
  -> post-run data quality checks
  -> monitoring/alerts
```

## 6. How It Works Step By Step

1. Unit test transformation functions.
2. Validate schemas.
3. Run sample integration tests.
4. Check row counts and uniqueness.
5. Check nulls, ranges, accepted values.
6. Compare key metrics to expectations.
7. Run end-to-end tests for critical pipelines.
8. Alert/quarantine on failures.

## 7. How To Use It Practically

Common test types:

| Test Type | Example |
|---|---|
| unit | function maps status correctly |
| schema | column exists and has expected type |
| uniqueness | customer_id unique in dimension |
| not null | order_id cannot be null |
| range | amount >= 0 |
| relationship | fact customer_key exists in dim_customer |
| freshness | table updated within 1 hour |
| regression | revenue total did not drop unexpectedly |

## 8. Real-World Scenario

- Product/system: Payment analytics pipeline.
- Problem: A join bug duplicates payment rows.
- How tests help: uniqueness and revenue anomaly checks catch the issue before dashboard refresh.
- What would go wrong without tests: finance reports inflated revenue.

## 9. System Design Angle

Testing strategy:

- fast tests in CI
- heavier tests after staging run
- production data quality checks after each run
- freshness checks for critical datasets
- alerting on business-impacting failures

Key phrase:

```text
Task success is not the same as data correctness.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| catches bad data early | tests require maintenance |
| builds trust | false positives can annoy teams |
| documents assumptions | full-data tests can cost money |
| supports safe changes | thresholds need tuning |

## 11. Failure Modes

- Failure: Tests too strict.
- Symptom: noisy failures.
- Recovery: tune thresholds.
- Prevention: use business-aware expectations.

- Failure: Tests too weak.
- Symptom: bad data passes.
- Recovery: add better checks.
- Prevention: learn from incidents.

- Failure: Tests not blocking release.
- Symptom: known bad data promoted.
- Recovery: enforce gates.
- Prevention: CI/CD and orchestration integration.

## 12. Common Mistakes

- Mistake: Only testing code, not data.
- Why it is wrong: data assumptions can break independently of code.
- Better approach: add schema and data quality tests.

- Mistake: Testing everything with full scans.
- Why it is wrong: expensive and slow.
- Better approach: combine sample, incremental, and critical full checks.

## 13. Mini Example

```text
orders table checks:
order_id not null
order_id unique
amount >= 0
order_date not in future
row count within expected range
```

## 14. Interview Questions

1. How do you test data pipelines?
2. Unit tests vs data quality tests?
3. What tests would you add for orders?
4. Why is task success insufficient?
5. How do you avoid noisy tests?

## 15. Interview Speak

"Data pipeline testing needs both software tests and data tests. I would test transformation logic, schemas, uniqueness, nulls, relationships, freshness, row counts, and key metric ranges. Critical checks should block deployment or downstream publishing."

## 16. Quick Recall

- One-line summary: Pipeline testing checks both code and produced data.
- Three keywords: schema, quality, freshness.
- One trap: Assuming successful task means correct data.
- One memory trick: Machine works, product still needs inspection.
