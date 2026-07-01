# Topic 191: Great Expectations

## 1. Goal

Understand Great Expectations as a data quality validation framework.

## 2. Baby Intuition

Great Expectations lets you write expectations about data.

Example: "order_id should not be null" or "status should be one of these valid values."

## 3. What It Is

- Simple definition: Great Expectations validates data against expectations.
- Technical definition: Great Expectations is an open-source data quality framework for defining, running, documenting, and reporting data validation rules called expectations across data sources.
- Category: Data quality testing framework.
- Related terms: expectation, expectation suite, checkpoint, data docs, validator, datasource.

## 4. Why It Exists

Data quality rules are often hidden in people's heads or scattered SQL.

Great Expectations exists to:

- make rules explicit
- run validations automatically
- document expectations
- generate human-readable data docs
- integrate with pipelines
- fail or alert when data breaks rules

## 5. Where It Fits In A Data Platform

```text
pipeline produces dataset
  -> Great Expectations checkpoint validates data
  -> pass: downstream continues
  -> fail: alert/block/quarantine
```

It can be used with files, databases, warehouses, Spark, and orchestration tools.

## 6. How It Works Step By Step

1. Connect to a datasource.
2. Define expectations for a dataset.
3. Group expectations into a suite.
4. Run validation against actual data.
5. Produce validation result.
6. Generate documentation/report.
7. Trigger pipeline action based on pass/fail.

## 7. How To Use It Practically

Example expectations:

```text
expect_column_values_to_not_be_null("order_id")
expect_column_values_to_be_between("amount", min_value=0)
expect_column_values_to_be_in_set("status", ["created", "paid", "cancelled"])
expect_table_row_count_to_be_between(min_value=1000, max_value=2000000)
```

Use for:

- source validation
- post-transform checks
- pre-publish checks
- contract enforcement
- documentation

## 8. Real-World Scenario

- Product/system: Orders silver table.
- Problem: Bad upstream deploy sends null order IDs.
- How Great Expectations helps: not-null expectation fails and blocks publishing to gold mart.
- What would go wrong without it: dashboard and downstream joins break.

## 9. System Design Angle

Use Great Expectations when:

- data quality rules need documentation
- validations should run in pipelines
- teams need readable validation reports
- data contracts need enforcement
- critical datasets require gates

Be careful with:

- test noise
- expensive full-table validations
- expectation maintenance
- thresholds for real-world messy data

## 10. Trade-offs

| Pros | Cons |
|---|---|
| explicit quality rules | setup/maintenance effort |
| readable docs | can be noisy if rules are unrealistic |
| pipeline integration | full scans may cost money |
| many built-in expectations | custom expectations may be needed |

## 11. Failure Modes

- Failure: Too strict expectations.
- Symptom: frequent false failures.
- Recovery: adjust thresholds.
- Prevention: use historical baselines and business input.

- Failure: Expectations not run in production.
- Symptom: rules exist but do not protect data.
- Recovery: integrate checkpoints with orchestrator.
- Prevention: CI/runtime gates.

- Failure: Full-table validation too expensive.
- Symptom: slow/costly pipelines.
- Recovery: sample or partition checks.
- Prevention: choose validation scope carefully.

## 12. Common Mistakes

- Mistake: Writing expectations but not attaching them to pipeline flow.
- Why it is wrong: bad data still moves downstream.
- Better approach: run checkpoints before publish.

- Mistake: Expecting all data quality to be solved by one tool.
- Why it is wrong: quality also needs ownership, contracts, monitoring, and incident response.
- Better approach: use GX as one part of DataOps.

## 13. Mini Example

```text
orders_silver checkpoint:
order_id not null
order_id unique
amount >= 0
status in accepted values
updated_at freshness within 1 day
```

## 14. Interview Questions

1. What is Great Expectations?
2. What is an expectation?
3. How does it fit into pipelines?
4. What happens on validation failure?
5. How do you avoid noisy expectations?

## 15. Interview Speak

"Great Expectations is a data quality framework for defining and running validation rules called expectations. I would use it as a pipeline gate for important datasets, with expectations around nulls, uniqueness, ranges, accepted values, row counts, and freshness, while tuning thresholds to avoid noisy false positives."

## 16. Quick Recall

- One-line summary: Great Expectations checks whether data meets explicit rules.
- Three keywords: expectation, checkpoint, data docs.
- One trap: Rules that are never run in production.
- One memory trick: Write what good data should look like.
