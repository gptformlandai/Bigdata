# Topic 267: Design Data Warehouse For Finance Reporting

## 1. Goal

Design a finance reporting warehouse that provides accurate, governed, auditable metrics like revenue, cost, invoices, payments, and close reports.

## 2. Baby Intuition

Finance reporting is not a casual dashboard.

It is the official ledger view where numbers must be explainable, reconciled, and consistent.

## 3. Requirements

Clarify:

- Which reports: revenue, bookings, invoices, payments, GL, tax?
- How often are reports refreshed?
- What is the close process?
- Which systems are sources of truth?
- What audit/compliance requirements exist?

## 4. Functional Requirements

- ingest data from ERP, billing, payment, CRM, order systems
- model facts and dimensions
- support historical changes through SCDs
- reconcile warehouse numbers with source systems
- provide certified finance metrics
- support month-end close and audit extracts
- enforce strict access control

## 5. Non-Functional Requirements

- high correctness and auditability
- repeatable reports
- strong lineage
- controlled changes
- secure sensitive financial data
- predictable query performance
- reliable refresh SLAs

## 6. Capacity Estimation

Finance warehouses are often not the largest by event volume, but correctness is strict.

Example:

```text
100M invoices/year
500M payment transactions/year
daily incremental loads
monthly close reports with heavy joins
```

The main challenge is not raw scale. It is trust.

## 7. Events And APIs

Inputs:

- invoice_created
- payment_received
- refund_issued
- order_booked
- subscription_changed
- exchange_rate_loaded

Batch/CDC sources:

```text
billing_db.invoices
payments_db.transactions
erp.general_ledger
crm.accounts
```

## 8. Data Model

Star schema:

```text
fact_invoice(invoice_id, customer_key, product_key, date_key, amount, currency, status)
fact_payment(payment_id, invoice_id, date_key, amount, currency, method)
dim_customer(customer_key, customer_id, segment, region, valid_from, valid_to)
dim_product(product_key, product_id, product_family)
dim_date(date_key, calendar_date, fiscal_period)
```

Certified metric:

```text
recognized_revenue = finance-approved logic, versioned and documented
```

## 9. High-Level Architecture

```text
finance source systems
  -> ingestion/CDC
  -> staging tables
  -> validation and reconciliation
  -> dimensional warehouse
  -> certified marts
  -> finance dashboards, extracts, audit reports
```

## 10. Data Flow

1. Ingest source data into staging.
2. Validate row counts, totals, schema, and freshness.
3. Standardize currencies, dates, customer/product IDs.
4. Build dimensions with SCD handling.
5. Build fact tables for invoices, payments, revenue, costs.
6. Reconcile facts against source totals.
7. Publish certified marts after checks pass.
8. Finance users query reports and audit extracts.

## 11. Deep Dive Components

Reconciliation:

- source invoice count vs warehouse invoice count
- source payment total vs warehouse payment total
- revenue by period matches finance-approved result

Change management:

- version metric definitions
- code review for transformations
- approval workflow for certified marts
- backfill plan for logic changes

Audit:

- lineage from report to source
- who changed logic
- when report was generated
- source snapshot used

## 12. Scaling And Partitioning

- Partition fact tables by fiscal date/month.
- Cluster by customer/product/invoice IDs.
- Use materialized views or aggregate tables for common reports.
- Separate finance compute from ad hoc exploratory compute.
- Use incremental transformations for daily refresh.

## 13. Consistency And Correctness

- Use source systems as systems of record.
- Snapshot important inputs for repeatable reports.
- Handle late adjustments and reversals.
- Use SCD Type 2 for historical dimensions when needed.
- Do not publish reports before reconciliation passes.

## 14. Failure Handling

| Failure | Handling |
|---|---|
| source file late | delay publish and notify finance |
| reconciliation mismatch | block certified mart publish |
| bad exchange rate | quarantine and rerun |
| dimension mapping missing | reject/exception queue |
| metric logic bug | rollback version and restate affected periods |

## 15. Monitoring, Cost, And Security

Monitor:

- source freshness
- reconciliation differences
- refresh duration
- failed quality checks
- report query latency
- access to sensitive finance data

Cost:

- incremental loads
- aggregate common reports
- archive old staging data
- warehouse workload management

Security:

- restrict finance data by role
- mask bank/tax identifiers
- audit report access
- encrypt sensitive data
- separate SOX/audit-controlled transformations where required

## 16. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| strict reconciliation | high trust | slower publish |
| dimensional model | easy reporting | modeling effort |
| SCD history | correct historical reporting | more complex joins |
| certified marts | consistent metrics | slower change process |

## 17. Interview-Ready Final Answer

"I would design the finance warehouse around correctness and auditability. Source systems like billing, payments, ERP, and CRM feed staging tables through batch or CDC. Validation and reconciliation checks compare counts and totals against sources before data is transformed into dimensional fact and dimension tables. Certified marts expose approved metrics such as revenue and payments. I would use SCDs, fiscal calendar dimensions, source snapshots, lineage, metric versioning, access controls, and publish gates so finance reports are repeatable and auditable."

## 18. Quick Recall

- One-line summary: Finance warehouse optimizes for trusted, reconciled, auditable numbers.
- Core tools: staging, reconciliation, star schema, SCDs, certified marts, lineage.
- Main trap: treating finance metrics like casual product analytics.
- Memory trick: official ledger, not a loose dashboard.

