# Topic 013: SQL Basics

## Goal

Understand SQL as the main language for querying structured data and the foundation for analytics, warehouses, Spark SQL, dbt, dashboards, and interviews.

## Simple Explanation

SQL is how we ask questions from tables.

Example:

```text
From the orders table, show me total revenue per day.
```

In SQL:

```sql
SELECT
    DATE(created_at) AS order_date,
    SUM(amount) AS revenue
FROM orders
WHERE status = 'paid'
GROUP BY DATE(created_at);
```

## Core Idea

- Definition: SQL is a declarative language for querying and manipulating relational data.
- Why it matters: Most data platforms expose SQL because it is readable, powerful, and widely understood.
- Related terms: table, row, column, filter, join, aggregate, CTE, window function.

## Basic Clauses

| Clause | Purpose |
|---|---|
| `SELECT` | choose columns or expressions |
| `FROM` | choose table |
| `WHERE` | filter rows before aggregation |
| `GROUP BY` | group rows for aggregation |
| `HAVING` | filter groups after aggregation |
| `ORDER BY` | sort result |
| `LIMIT` | restrict number of rows |
| `JOIN` | combine tables |

Execution idea:

```text
FROM/JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
```

## How It Is Used

Data engineers use SQL for:

- dashboards
- warehouse models
- data validation
- pipeline transformations
- ad hoc analysis
- data quality checks
- backfills and reconciliation

Common tools:

- PostgreSQL
- MySQL
- Snowflake
- BigQuery
- Redshift
- Spark SQL
- Hive
- Trino/Presto
- dbt

## Essential Patterns

Filter:

```sql
SELECT *
FROM orders
WHERE status = 'paid';
```

Aggregate:

```sql
SELECT customer_id, SUM(amount) AS total_spend
FROM orders
GROUP BY customer_id;
```

Join:

```sql
SELECT
    o.order_id,
    c.customer_name,
    o.amount
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id;
```

Common table expression:

```sql
WITH paid_orders AS (
    SELECT *
    FROM orders
    WHERE status = 'paid'
)
SELECT customer_id, COUNT(*) AS paid_order_count
FROM paid_orders
GROUP BY customer_id;
```

## Big Data / System Design Angle

SQL at scale is still SQL, but execution changes.

In distributed engines:

- scans may read many files
- joins may trigger shuffles
- aggregations may require repartitioning
- bad filters can scan huge datasets
- partition pruning can save massive cost

Interview trigger words:

- reporting
- analytics
- dashboard
- data warehouse
- BI
- ad hoc query

## Common Mistakes

- Mistake: Using `SELECT *` on huge tables.
- Better way: Select only needed columns.

- Mistake: Forgetting join cardinality.
- Better way: Understand one-to-one, one-to-many, and many-to-many joins.

- Mistake: Filtering after aggregation when row-level filtering was intended.
- Better way: Use `WHERE` before `GROUP BY`; use `HAVING` for aggregate filters.

- Mistake: Ignoring partitions.
- Better way: Filter on partition columns like date when querying large tables.

## Interview Speak

"SQL is the standard way to query structured data. For Big Data, I still write SQL, but I think about execution: scan size, partition pruning, joins, shuffles, aggregations, and whether the query reads only the columns and partitions it needs."

## Quick Recall

- One-liner: SQL asks questions from tables.
- Keywords: select, join, group by.
- Trap: Writing correct SQL that is extremely expensive at scale.
