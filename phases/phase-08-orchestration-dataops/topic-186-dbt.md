# Topic 186: dbt

## 1. Goal

Understand dbt as a transformation and analytics engineering tool for warehouses/lakehouses.

## 2. Baby Intuition

dbt is like version-controlled SQL with tests and documentation.

It helps teams transform raw data into clean analytics models using software engineering habits.

## 3. What It Is

- Simple definition: dbt builds and tests SQL data models.
- Technical definition: dbt is an analytics engineering tool that uses SQL/Jinja models, dependency graphs, tests, documentation, macros, and environments to transform data inside warehouses or lakehouse query engines.
- Category: Transformation / analytics engineering tool.
- Related terms: model, source, ref, test, macro, materialization, lineage, seed, snapshot.

## 4. Why It Exists

Warehouse transformations used to be scattered:

- SQL in dashboards
- SQL in scripts
- SQL in stored procedures
- no tests
- no docs
- no lineage
- hard to review changes

dbt exists to make analytical SQL modular, testable, documented, and version-controlled.

## 5. Where It Fits In A Data Platform

```text
raw/staging tables in warehouse/lakehouse
  -> dbt models transform data
  -> marts/semantic tables
  -> BI dashboards and analysts
```

dbt does not usually extract data from sources. It transforms data already in the warehouse/lakehouse.

## 6. How It Works Step By Step

1. Define sources.
2. Write SQL models.
3. Use `ref()` to declare dependencies.
4. dbt builds a DAG of models.
5. dbt compiles SQL with Jinja/macros.
6. dbt runs models in dependency order.
7. dbt runs tests.
8. dbt generates docs and lineage.

## 7. How To Use It Practically

Model layers:

| Layer | Meaning |
|---|---|
| sources | raw external tables |
| staging | clean/rename/cast source fields |
| intermediate | reusable business logic |
| marts | business-ready facts/dimensions/aggregates |

Example:

```sql
select
  order_id,
  customer_id,
  cast(order_ts as timestamp) as order_ts,
  amount
from {{ source('app', 'orders') }}
```

Common tests:

- not null
- unique
- accepted values
- relationships
- custom business checks

## 8. Real-World Scenario

- Product/system: Revenue analytics mart.
- Problem: Revenue SQL is duplicated across dashboards.
- How dbt helps: centralize revenue logic in version-controlled models with tests and docs.
- What would go wrong without it: each dashboard calculates revenue differently.

## 9. System Design Angle

Use dbt when:

- transformations are mostly SQL
- warehouse/lakehouse is main compute layer
- analytics models need tests/docs/lineage
- team practices code review
- BI metrics need governance

Be careful with:

- very heavy non-SQL processing
- poorly layered models
- overusing Jinja
- slow model builds
- unclear ownership

## 10. Trade-offs

| Pros | Cons |
|---|---|
| version-controlled SQL | not an ingestion tool |
| tests and docs | SQL-heavy |
| lineage graph | can create too many models |
| modular transformations | warehouse cost depends on builds |
| strong analytics engineering workflow | complex macros can be hard to debug |

## 11. Failure Modes

- Failure: Test failures ignored.
- Symptom: bad data reaches marts.
- Recovery: stop promotion and fix data/model.
- Prevention: CI/CD gates.

- Failure: Model dependency explosion.
- Symptom: slow builds and hard lineage.
- Recovery: refactor layers.
- Prevention: modeling standards.

- Failure: Full refresh of huge model.
- Symptom: expensive/slow run.
- Recovery: incremental materialization.
- Prevention: choose materialization carefully.

## 12. Common Mistakes

- Mistake: Putting all business logic in one giant model.
- Why it is wrong: hard to test and reuse.
- Better approach: use layered staging/intermediate/mart models.

- Mistake: Treating dbt as a scheduler.
- Why it is wrong: dbt runs transformations; orchestration often comes from Airflow/Dagster/Prefect/dbt Cloud jobs.
- Better approach: use dbt with an orchestrator for full pipeline dependencies.

## 13. Mini Example

```text
source app.orders
  -> stg_orders
  -> int_order_revenue
  -> fct_orders
  -> mart_daily_revenue
```

## 14. Interview Questions

1. What is dbt?
2. What problem does dbt solve?
3. What is `ref()`?
4. What tests does dbt support?
5. dbt vs Airflow?

## 15. Interview Speak

"dbt is an analytics engineering tool for transforming warehouse/lakehouse data using version-controlled SQL. It creates a model dependency graph, supports tests, docs, macros, and materializations, and is best for SQL transformations after data has landed."

## 16. Quick Recall

- One-line summary: dbt makes SQL transformations modular, tested, and documented.
- Three keywords: models, tests, lineage.
- One trap: Treating dbt as ingestion or full orchestration.
- One memory trick: Software engineering for SQL models.
