# Phase 7 Review: Warehouses And Query Engines

## 1. Phase Summary

Phase 7 explains the analytical systems that serve SQL, BI, dashboards, reports, and business metrics.

The core idea:

```text
business questions need trusted, fast, governed analytical tables
warehouses store/model them
query engines plan and execute SQL
OLAP serving stores power low-latency dashboards/APIs
```

If you remember only one sentence:

```text
Warehouses and query engines exist so large historical data can be queried with SQL without hurting operational systems.
```

## 2. Big Picture

```text
Sources
  -> ingestion / CDC / batch loads
  -> staging/raw data
  -> facts, dimensions, marts, aggregates
  -> warehouse/query engine/OLAP store
  -> BI, dashboards, analysts, APIs, ML
```

## 3. Tool Comparison

| Tool | Best Mental Model | Strong Fit | Watch Out |
|---|---|---|---|
| Snowflake | managed warehouse with separate compute | governed BI, workload isolation | compute cost and role design |
| BigQuery | serverless distributed SQL | GCP analytics, ad hoc SQL | scanned data and partition filters |
| Redshift | AWS MPP warehouse | AWS BI/reporting | distribution/sort key choices |
| Synapse | Azure analytics workspace | Azure SQL/lake/Power BI integration | choosing right compute mode |
| ClickHouse | fast columnar OLAP database | event/log dashboards | order key and OLTP misuse |
| Druid | realtime indexed event analytics | live time-series dashboards | segment/cardinality tuning |
| Pinot | user-facing OLAP serving | low-latency analytics APIs | index/table design |
| Trino | distributed/federated SQL engine | lakehouse and multi-source SQL | cross-source joins and memory |
| Athena | serverless SQL over S3 | ad hoc lake queries | raw files and small files |

## 4. Warehouse Vs Lakehouse Vs Query Engine

| System Type | Owns Storage? | Main Use |
|---|---|---|
| warehouse | usually yes/platform-managed | trusted BI and reporting |
| lakehouse | open object storage plus table format | open analytics storage for many engines |
| query engine | often no | run SQL over external data |
| OLAP serving store | yes/specialized | low-latency dashboards/APIs |

Simple memory:

```text
warehouse = managed SQL home
lakehouse = open table layer on lake storage
query engine = SQL brain over sources
OLAP serving store = fast dashboard/API backend
```

## 5. Core Internal Concepts

| Concept | Meaning | Why It Matters |
|---|---|---|
| columnar storage | store data by column | read fewer bytes for analytics |
| MPP | many workers process query | scale large scans/aggregations |
| query planning | SQL to execution plan | explains how queries actually run |
| CBO | chooses plan using stats | affects join order and scan strategy |
| predicate pushdown | apply filters near storage | reduces scanned data |
| projection pruning | read only needed columns | reduces bytes and cost |
| data movement | exchange/shuffle between workers | often a bottleneck |
| skew | uneven data distribution | one worker becomes slow |

## 6. Columnar Storage

Columnar storage is ideal for:

- large scans
- aggregates
- dashboards
- reading a few columns from many rows
- compression

Strong line:

> Row stores are good for transactions. Column stores are good for analytics.

Common mistake:

```text
SELECT * FROM huge_table
```

This removes many benefits of column pruning.

## 7. MPP Architecture

MPP execution:

```text
coordinator creates plan
workers scan partitions/splits
workers filter and aggregate locally
workers exchange data for joins/groups
coordinator merges final result
```

Performance risks:

- data skew
- huge shuffle
- bad distribution key
- too many small files
- memory-heavy joins

Interview line:

> MPP speeds up big scans, but data movement can dominate if joins and distribution are poorly designed.

## 8. Query Planning And CBO

Query planning decides:

- scan order
- filters
- joins
- aggregations
- sorts
- exchanges
- physical operators

The cost-based optimizer uses:

- row counts
- file/table size
- column stats
- selectivity
- cardinality
- join keys

Common fix:

```text
If the optimizer makes bad choices, inspect EXPLAIN and refresh statistics.
```

## 9. Precomputation

### Materialized Views

Materialized views store query results.

Use when:

- query is repeated
- query is expensive
- result is smaller than raw data
- slight staleness is acceptable

Trade-off:

```text
faster reads vs refresh/storage/staleness
```

### OLAP Cubes

Cubes precompute measures across dimensions.

Terms:

- measure: revenue, count, duration
- dimension: date, region, product
- roll-up: day to month
- drill-down: month to day
- slice/dice: filter dimensions

Risk:

```text
too many dimensions create cube explosion
```

## 10. Dimensional Modeling

The most important word:

```text
grain = what one row means
```

If grain is unclear, metrics become wrong.

### Fact Tables

Facts store:

- business events
- measures
- foreign keys to dimensions

Examples:

- one row per order line
- one row per click
- one row per account balance snapshot

### Dimension Tables

Dimensions store:

- descriptive attributes
- categories
- hierarchy
- business context

Examples:

- customer
- product
- date
- store
- region

## 11. Star Schema Vs Snowflake Schema

| Model | Meaning | Best For |
|---|---|---|
| star schema | fact table plus denormalized dimensions | simple BI and fast joins |
| snowflake schema | normalized dimensions with sub-dimensions | complex hierarchies and less duplication |

Practical default:

```text
Prefer star schema for BI simplicity unless normalized dimensions solve a real problem.
```

## 12. Slowly Changing Dimensions

SCDs answer:

```text
When a dimension value changes, should history change too?
```

| Type | Behavior | Use |
|---|---|---|
| Type 1 | overwrite old value | corrections |
| Type 2 | create version rows | historical reporting |
| Type 3 | store limited previous value | simple before/after tracking |

Type 2 columns:

```text
surrogate_key
business_key
effective_start
effective_end
is_current
```

## 13. Warehouse Design Checklist

For a warehouse/mart, define:

- business process
- fact grain
- measures
- dimensions
- SCD behavior
- data freshness SLA
- quality tests
- ownership
- metric definitions
- access control
- partitioning/clustering
- aggregate/materialized views
- cost monitoring

## 14. Slow Query Checklist

When a warehouse query is slow:

1. Check scanned bytes.
2. Check partition filters.
3. Check selected columns.
4. Inspect EXPLAIN plan.
5. Look for huge joins/shuffles.
6. Check table statistics.
7. Check data skew.
8. Check small files if querying lake data.
9. Consider materialized views/aggregates.
10. Consider model redesign.

## 15. Common Interview Questions

1. What is a data warehouse?
2. Why not query OLTP databases directly?
3. Snowflake vs BigQuery vs Redshift?
4. What is ClickHouse/Druid/Pinot good for?
5. What is Trino?
6. What is Athena?
7. Why is columnar storage fast for analytics?
8. What is MPP?
9. What is query planning?
10. What does a cost-based optimizer use?
11. What is a materialized view?
12. What is an OLAP cube?
13. Star schema vs snowflake schema?
14. Fact vs dimension?
15. SCD Type 1 vs Type 2?

## 16. Strong System Design Answer

Question:

> Design an analytics platform for an e-commerce company.

Strong answer:

"I would keep operational databases focused on transactions and build an analytical platform separately. Data would be ingested through CDC and batch loads into raw/staging tables. Transformations would clean and model data into facts such as orders, payments, and clicks, plus dimensions such as customer, product, date, and region.

For business reporting, I would use a cloud warehouse such as Snowflake, BigQuery, Redshift, or Synapse depending on cloud and team context. For low-latency product-facing analytics, I would consider ClickHouse, Druid, or Pinot. For lakehouse SQL across open tables, I would consider Trino or Athena.

Performance would come from columnar storage, partitioning/clustering, good fact grain, materialized views for repeated dashboards, and cost-based query planning with fresh statistics. I would monitor freshness, data quality, query cost, scanned bytes, slow dashboards, and access control."

## 17. Hands-On Project

Build a small warehouse mart locally:

1. Create raw CSV data for orders, customers, and products.
2. Create a fact_orders table.
3. Create dim_customer, dim_product, and dim_date.
4. Write SQL queries for revenue by month, product category, and customer segment.
5. Add a materialized-view-like aggregate table for daily revenue.
6. Simulate an SCD Type 2 customer segment change.
7. Compare raw query vs aggregate query.

What this teaches:

- grain
- facts and dimensions
- star schema
- precomputation
- history handling
- dashboard-friendly modeling

## 18. Quick Revision Cards

| Prompt | Answer |
|---|---|
| Warehouse? | managed analytical SQL system for BI/reporting |
| Columnar? | stores values by column for fast scans |
| MPP? | many workers execute one query |
| CBO? | optimizer chooses plan using stats |
| Materialized view? | stored query result |
| Cube? | precomputed measures across dimensions |
| Star schema? | central fact plus dimensions |
| Snowflake schema? | normalized dimensions |
| Fact? | event/measure table |
| Dimension? | descriptive context table |
| Grain? | what one row means |
| SCD Type 1? | overwrite |
| SCD Type 2? | version history |
