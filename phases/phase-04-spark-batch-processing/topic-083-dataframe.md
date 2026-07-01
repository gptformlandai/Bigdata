# Topic 083: DataFrame

## 1. Goal

Understand DataFrames as Spark's main high-level API for structured data processing.

## 2. Baby Intuition

A DataFrame is like a table or spreadsheet spread across many machines.

It has rows and columns, but it can be huge and distributed.

## 3. What It Is

- Simple definition: A DataFrame is a distributed table with named columns.
- Technical definition: A Spark DataFrame is a distributed collection of rows organized into named columns, backed by Spark SQL's logical/physical planning and Catalyst optimization.
- Category: High-level structured API.
- Related terms: schema, row, column, Spark SQL, Catalyst, Dataset, transformation.

## 4. Why It Exists

RDDs are powerful but low-level.

DataFrames exist because most data engineering work is structured:

- tables
- columns
- filters
- joins
- aggregations
- SQL transformations

DataFrames let Spark understand your data structure and optimize the plan.

## 5. Where It Fits In A Data Platform

```text
Files/Tables -> DataFrame transformations -> Curated tables/files
```

DataFrames are used for:

- ETL
- cleaning
- joins
- aggregations
- SQL analytics
- lakehouse transformations

## 6. How It Works Step By Step

Example:

```python
orders = spark.read.parquet("/data/orders")

paid = orders.where("status = 'paid'")

revenue = paid.groupBy("customer_id").sum("amount")
```

What Spark sees:

1. table schema
2. filter condition
3. groupBy key
4. aggregation expression
5. possible optimization opportunities

Spark can optimize because operations are expressed structurally, not as opaque Python functions.

## 7. How To Use It Practically

Read data:

```python
df = spark.read.parquet("/data/orders")
```

Inspect:

```python
df.printSchema()
df.show(10)
df.select("order_id", "amount").show()
```

Transform:

```python
from pyspark.sql.functions import col, sum as spark_sum

result = (
    df
    .where(col("status") == "paid")
    .groupBy("customer_id")
    .agg(spark_sum("amount").alias("revenue"))
)
```

Write:

```python
result.write.mode("overwrite").parquet("/data/customer_revenue")
```

## 8. Real-World Scenario

- Product/system: Daily customer metrics pipeline.
- Problem: Need to join orders, clicks, and profile tables.
- How DataFrame helps: Provides table-like API with optimizer support.
- What would go wrong without it: RDD code would be verbose and harder to optimize.

## 9. System Design Angle

Use DataFrames for:

- structured/semi-structured data
- SQL-like ETL
- production pipelines
- optimized joins and aggregations
- Parquet/ORC/lakehouse tables

DataFrames improve:

- developer productivity
- optimization
- readability
- interoperability with SQL

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| optimizer support | less low-level control |
| schema awareness | schema management needed |
| concise APIs | UDFs can reduce optimization |
| SQL interoperability | debugging plans takes practice |

## 11. Failure Modes

- Failure: Schema mismatch.
- Symptom: read/query fails or nulls appear.
- Recovery: fix schema or cast fields.
- Prevention: schema validation.

- Failure: Python UDF overuse.
- Symptom: slow jobs.
- Recovery: replace with built-in functions.
- Prevention: prefer Spark SQL functions.

- Failure: Huge join without strategy.
- Symptom: shuffle explosion.
- Recovery: broadcast small table, partition, or optimize join.
- Prevention: understand data sizes.

## 12. Common Mistakes

- Mistake: Treating DataFrame like pandas.
- Why it is wrong: Spark DataFrame is distributed and lazy.
- Better approach: use distributed operations and avoid driver collection.

- Mistake: Using Python loops over rows.
- Why it is wrong: destroys distributed processing benefits.
- Better approach: use column expressions and built-in functions.

## 13. Mini Example

```python
df.select("customer_id", "amount").where("amount > 100")
```

This is not immediately executed. It builds a plan.

An action triggers it:

```python
df.count()
```

## 14. Interview Questions

1. What is a Spark DataFrame?
2. Why are DataFrames preferred over RDDs for structured data?
3. What is a schema?
4. Why are UDFs sometimes slow?
5. DataFrame vs pandas DataFrame?

## 15. Interview Speak

"A Spark DataFrame is a distributed table with named columns. It is preferred for structured ETL because Spark understands the schema and operations, allowing Catalyst to optimize filters, projections, joins, and aggregations. Unlike pandas, Spark DataFrames are distributed and lazy."

## 16. Quick Recall

- One-line summary: DataFrame is a distributed optimized table.
- Three keywords: schema, columns, Catalyst.
- One trap: Treating it like local pandas.
- One memory trick: DataFrame is SQL table thinking in Spark.
