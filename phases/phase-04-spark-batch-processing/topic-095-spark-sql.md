# Topic 095: Spark SQL

## 1. Goal

Understand Spark SQL as Spark's SQL engine for querying structured data.

## 2. Baby Intuition

Spark SQL lets you talk to huge distributed data using SQL.

Instead of writing many DataFrame operations, you can ask:

```sql
SELECT customer_id, SUM(amount)
FROM orders
GROUP BY customer_id
```

Spark turns that SQL into a distributed execution plan.

## 3. What It Is

- Simple definition: Spark SQL lets Spark run SQL queries on distributed data.
- Technical definition: Spark SQL is Spark's module for structured data processing, providing SQL queries, DataFrame operations, catalog integration, and optimizer support through Catalyst.
- Category: SQL engine / structured processing.
- Related terms: DataFrame, SparkSession, Catalyst, table, view, catalog.

## 4. Why It Exists

Many data users know SQL.

Big Data teams need SQL for:

- ETL transformations
- analytics
- reporting
- joins and aggregations
- table creation
- lakehouse processing

Spark SQL exists so users can process huge datasets with familiar SQL while Spark handles distributed execution.

## 5. Where It Fits In A Data Platform

```text
Data Lake/Warehouse Tables -> Spark SQL -> Curated Tables/Reports/Features
```

Spark SQL can query:

- temporary views
- Hive tables
- Parquet files
- ORC files
- JSON/CSV
- lakehouse tables depending on connectors

## 6. How It Works Step By Step

1. User writes SQL.
2. Spark parses SQL.
3. Spark analyzes table/column references.
4. Catalyst optimizes the logical plan.
5. Spark creates a physical plan.
6. Executors run distributed tasks.
7. Results return or write to storage.

## 7. How To Use It Practically

Create view:

```python
orders = spark.read.parquet("/data/orders")
orders.createOrReplaceTempView("orders")
```

Run SQL:

```python
result = spark.sql("""
SELECT customer_id, SUM(amount) AS revenue
FROM orders
WHERE status = 'paid'
GROUP BY customer_id
""")
```

Use SQL directly:

```sql
CREATE TABLE customer_revenue AS
SELECT customer_id, SUM(amount) AS revenue
FROM orders
GROUP BY customer_id;
```

## 8. Real-World Scenario

- Product/system: Finance reporting ETL.
- Problem: Analysts and engineers need shared transformation logic.
- How Spark SQL helps: SQL is readable and runs distributed over large tables.
- What would go wrong without it: Teams may write custom code for logic that is naturally relational.

## 9. System Design Angle

Spark SQL is strong when:

- transformations are relational
- teams prefer SQL
- data is structured
- queries need distributed scale
- pipeline uses tables/lakehouse

Watch for:

- large joins
- missing partition filters
- UDFs blocking optimization
- poor file layout

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| SQL productivity | query tuning still needed |
| optimizer support | bad SQL can still be expensive |
| DataFrame interoperability | catalog/config complexity |
| broad user access | governance needed |

## 11. Failure Modes

- Failure: SQL scans too much data.
- Symptom: slow query and high cost.
- Recovery: add filters/partitions/projection.
- Prevention: table design and query review.

- Failure: Unsupported/slow UDF.
- Symptom: optimizer cannot improve logic.
- Recovery: use built-in functions.
- Prevention: avoid UDFs where possible.

## 12. Common Mistakes

- Mistake: Assuming SQL is automatically optimized enough.
- Why it is wrong: query shape and data layout still matter.
- Better approach: inspect physical plan.

- Mistake: Forgetting DataFrame and SQL share engine.
- Why it is wrong: both use Catalyst.
- Better approach: choose API based on readability and team needs.

## 13. Mini Example

```python
df_api = orders.groupBy("customer_id").sum("amount")

sql_api = spark.sql("""
SELECT customer_id, SUM(amount)
FROM orders
GROUP BY customer_id
""")
```

Both can use the same optimizer.

## 14. Interview Questions

1. What is Spark SQL?
2. How is Spark SQL related to DataFrames?
3. What is a temp view?
4. How do you inspect a Spark SQL plan?
5. Why can SQL still be slow?

## 15. Interview Speak

"Spark SQL is Spark's structured query engine. It lets users run SQL over distributed files and tables, and it uses the same Catalyst optimizer as DataFrames. It is powerful for ETL and analytics, but performance still depends on partitioning, file format, joins, and avoiding unnecessary scans."

## 16. Quick Recall

- One-line summary: Spark SQL runs SQL as distributed Spark jobs.
- Three keywords: SQL, DataFrame, Catalyst.
- One trap: Thinking SQL removes performance tuning.
- One memory trick: SQL is the language; Spark is the engine.
