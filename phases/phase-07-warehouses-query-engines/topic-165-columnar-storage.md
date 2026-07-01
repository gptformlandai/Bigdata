# Topic 165: Columnar Storage

## 1. Goal

Understand why analytical systems store data by columns instead of rows.

## 2. Baby Intuition

If you only need the `amount` column, why read every customer's name, address, and note?

Columnar storage lets analytics read the columns needed for the question.

## 3. What It Is

- Simple definition: Columnar storage stores values from the same column together.
- Technical definition: Columnar storage organizes data by column rather than row, enabling efficient compression, vectorized scans, column pruning, and analytical aggregation.
- Category: Analytical storage layout.
- Related terms: Parquet, ORC, ClickHouse, BigQuery, Snowflake, Redshift, compression, vectorization.

## 4. Why It Exists

Analytics queries often read:

- many rows
- few columns
- aggregates like SUM/COUNT/AVG
- filters on selected columns

Row storage is good for OLTP because one transaction often needs one full row.

Columnar storage is good for OLAP because queries often need only some columns across many rows.

## 5. Where It Fits In A Data Platform

```text
OLAP warehouse/lakehouse/query engine
  -> stores/scans data by column
  -> reads fewer bytes for analytical SQL
```

Used in:

- Parquet/ORC files
- BigQuery
- Snowflake internals
- Redshift
- ClickHouse
- Druid/Pinot

## 6. How It Works Step By Step

Row format:

```text
row1: id, date, amount, country
row2: id, date, amount, country
```

Columnar format:

```text
id column:      1, 2, 3
date column:    ...
amount column:  ...
country column: ...
```

For:

```sql
SELECT SUM(amount) FROM orders;
```

the engine mainly reads the `amount` column.

## 7. How To Use It Practically

Write analytical lake data in columnar formats:

- Parquet
- ORC

Query habits:

- avoid unnecessary `SELECT *`
- select required columns
- filter early
- use partitioning and clustering with column stats
- compress data

## 8. Real-World Scenario

- Product/system: Orders dashboard.
- Problem: Dashboard needs total revenue by day from billions of orders.
- How columnar storage helps: engine reads date and amount columns, not every column.
- What would go wrong with row-heavy scans: more bytes read, slower queries, higher cost.

## 9. System Design Angle

Columnar storage matters when:

- data is analytical
- scans are large
- queries use aggregates
- only a subset of columns is needed
- compression and scan cost matter

Avoid for:

- high-frequency single-row updates
- OLTP workloads
- tiny operational lookups

## 10. Trade-offs

| Pros | Cons |
|---|---|
| reads fewer columns | poor fit for OLTP row updates |
| better compression | writes may be more complex |
| fast aggregations | reconstructing full rows can cost more |
| vectorized execution | small point lookups may not benefit |

## 11. Failure Modes

- Failure: Users run `SELECT *`.
- Symptom: column pruning benefit lost.
- Recovery: select only needed columns.
- Prevention: query standards and semantic tables.

- Failure: Too many tiny columnar files.
- Symptom: metadata/open overhead.
- Recovery: compaction.
- Prevention: target good file sizes.

- Failure: Bad compression choice.
- Symptom: high storage or CPU cost.
- Recovery: choose codec for workload.
- Prevention: benchmark common queries.

## 12. Common Mistakes

- Mistake: Saying columnar is always faster.
- Why it is wrong: OLTP point updates/lookups may be better in row stores.
- Better approach: match storage layout to workload.

- Mistake: Using CSV for curated analytics.
- Why it is wrong: CSV is row/text format and scans parse too much.
- Better approach: use Parquet/ORC or warehouse-native columnar storage.

## 13. Mini Example

```text
Table has 100 columns.
Query needs 3 columns.

Columnar engine can read about those 3 column chunks,
instead of all 100 columns for every row.
```

## 14. Interview Questions

1. What is columnar storage?
2. Why is it good for analytics?
3. Columnar vs row storage?
4. Why is `SELECT *` bad?
5. How does compression help columnar data?

## 15. Interview Speak

"Columnar storage stores values from the same column together, which is ideal for OLAP queries that scan many rows but only a few columns. It improves compression, column pruning, vectorized execution, and aggregate performance, but it is not the best fit for OLTP point updates."

## 16. Quick Recall

- One-line summary: Columnar storage reads only the columns analytics needs.
- Three keywords: pruning, compression, aggregation.
- One trap: Using columnar for OLTP row updates.
- One memory trick: Do not read address when you only need revenue.
