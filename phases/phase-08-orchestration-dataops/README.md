# Phase 8: Orchestration And DataOps

Phase 8 teaches how production data pipelines are scheduled, tested, monitored, deployed, and operated.

The mental model is:

```text
data work is not just code
  -> it must run in the right order
  -> on a schedule or trigger
  -> with retries, tests, alerts, ownership, and incident response
```

This phase turns pipeline knowledge into production engineering knowledge.

## Topics

| # | Topic | Status |
|---:|---|---|
| 176 | Apache Airflow | Complete |
| 177 | DAGs | Complete |
| 178 | Airflow scheduler | Complete |
| 179 | Airflow executor | Complete |
| 180 | Sensors | Complete |
| 181 | Backfills | Complete |
| 182 | Retries | Complete |
| 183 | SLAs | Complete |
| 184 | Dagster | Complete |
| 185 | Prefect | Complete |
| 186 | dbt | Complete |
| 187 | CI/CD for data pipelines | Complete |
| 188 | Data pipeline testing | Complete |
| 189 | Data contracts | Complete |
| 190 | Data observability | Complete |
| 191 | Great Expectations | Complete |
| 192 | Monte Carlo/Datafold-style observability concepts | Complete |
| 193 | Pipeline monitoring | Complete |
| 194 | Alerting | Complete |
| 195 | Incident response for data pipelines | Complete |

## Phase Goal

By the end of this phase, you should be able to explain:

- why orchestration exists
- how Airflow DAGs, scheduler, executors, sensors, retries, backfills, and SLAs work
- how Dagster and Prefect differ from Airflow at a high level
- where dbt fits in modern analytics engineering
- how CI/CD, testing, data contracts, and observability make pipelines production-ready
- how monitoring, alerting, and incident response prevent small pipeline issues from becoming business outages

## Suggested Study Flow

1. Read Topics 176-183 for Airflow and orchestration fundamentals.
2. Read Topics 184-186 for Dagster, Prefect, and dbt.
3. Read Topics 187-191 for testing, contracts, observability, and Great Expectations.
4. Read Topics 192-195 for production monitoring and incident response.
5. Finish with `phase-08-review.md`.
