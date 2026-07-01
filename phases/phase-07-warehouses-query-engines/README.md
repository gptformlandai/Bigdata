# Phase 7: Warehouses And Query Engines

Phase 7 teaches analytical warehouses and query engines from baby steps to system-design depth.

The mental model is:

```text
data is stored in optimized analytical storage
  -> query engine plans SQL
  -> many workers scan/process in parallel
  -> results power dashboards, reports, analytics, and ML
```

Warehouses and query engines are where business users usually touch Big Data directly. They care about SQL, dashboards, cost, freshness, governance, and fast answers.

## Topics

| # | Topic | Status |
|---:|---|---|
| 155 | Data warehouse architecture | Complete |
| 156 | Snowflake | Complete |
| 157 | BigQuery | Complete |
| 158 | Redshift | Complete |
| 159 | Synapse | Complete |
| 160 | ClickHouse | Complete |
| 161 | Druid | Complete |
| 162 | Pinot | Complete |
| 163 | Presto/Trino | Complete |
| 164 | Athena | Complete |
| 165 | Columnar storage | Complete |
| 166 | MPP architecture | Complete |
| 167 | Query planning | Complete |
| 168 | Cost-based optimizer | Complete |
| 169 | Materialized views | Complete |
| 170 | OLAP cubes | Complete |
| 171 | Star schema | Complete |
| 172 | Snowflake schema | Complete |
| 173 | Fact and dimension tables | Complete |
| 174 | Slowly changing dimensions | Complete |
| 175 | Data modeling for analytics | Complete |

## Phase Goal

By the end of this phase, you should be able to explain:

- what a data warehouse is and why it exists
- how cloud warehouses like Snowflake, BigQuery, Redshift, and Synapse fit into a data platform
- how real-time/low-latency analytical stores like ClickHouse, Druid, and Pinot differ from batch warehouses
- how query engines like Trino and Athena query data lakes
- why columnar storage and MPP execution are central to analytics
- how query planning and cost-based optimization work at a high level
- how materialized views, cubes, star schemas, dimensions, facts, and SCDs support business analytics

## Suggested Study Flow

1. Read Topic 155 for the warehouse mental model.
2. Read Topics 156-164 for major warehouse/query engine tools.
3. Read Topics 165-168 for internal execution concepts.
4. Read Topics 169-170 for precomputation patterns.
5. Read Topics 171-175 for analytics modeling.
6. Finish with `phase-07-review.md`.
