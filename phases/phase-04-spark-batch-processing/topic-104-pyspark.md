# Topic 104: PySpark

## 1. Goal

Understand PySpark as the Python API for Spark and how to use it safely in production.

## 2. Baby Intuition

PySpark lets you write Python code while Spark does distributed work on the cluster.

You write:

```python
df.groupBy("customer_id").sum("amount")
```

Spark runs the heavy work across executors.

## 3. What It Is

- Simple definition: PySpark is Spark's Python interface.
- Technical definition: PySpark is the Python API for Apache Spark, allowing Python programs to create Spark sessions, use DataFrame/Spark SQL APIs, and submit distributed jobs to Spark clusters.
- Category: Spark development API.
- Related terms: SparkSession, DataFrame, UDF, pandas UDF, JVM, Py4J, executor.

## 4. Why It Exists

Many data engineers and analysts use Python.

PySpark exists so teams can use:

- Python syntax
- DataFrame API
- Spark SQL
- Python libraries for orchestration/glue logic
- distributed processing under the hood

Without PySpark, Python-first teams would need Scala/Java for Spark work.

## 5. Where It Fits In A Data Platform

```text
Python ETL code -> PySpark -> Spark cluster -> data lake/warehouse outputs
```

PySpark is common in:

- Databricks notebooks
- EMR jobs
- Glue jobs
- Airflow-submitted Spark jobs
- local development
- feature engineering

## 6. How It Works Step By Step

1. Python program creates SparkSession.
2. PySpark talks to Spark JVM engine.
3. DataFrame operations build a Spark plan.
4. Driver sends tasks to executors.
5. Executors process data.
6. Results are written or returned.

Important:

```text
PySpark DataFrame operations are distributed.
Normal Python loops are not automatically distributed.
```

## 7. How To Use It Practically

Basic PySpark job:

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum

spark = SparkSession.builder.appName("daily-revenue").getOrCreate()

orders = spark.read.parquet("/data/orders")

revenue = (
    orders
    .where(col("status") == "paid")
    .groupBy("dt")
    .agg(spark_sum("amount").alias("revenue"))
)

revenue.write.mode("overwrite").parquet("/data/revenue_by_day")
```

Prefer built-in functions:

```python
from pyspark.sql.functions import upper

df.select(upper(col("name")))
```

Be careful with Python UDFs:

```python
from pyspark.sql.functions import udf
```

UDFs can be slower because Spark optimizer has less visibility.

## 8. Real-World Scenario

- Product/system: Data engineering ETL.
- Problem: Team writes Python and needs to process TB-scale Parquet data.
- How PySpark helps: Python code expresses distributed transformations.
- What would go wrong without Spark understanding: local pandas/Python would not fit data in memory.

## 9. System Design Angle

PySpark is a developer API choice.

Use it when:

- team is Python-heavy
- data is too large for pandas
- Spark cluster is available
- ETL uses DataFrames/SQL

Avoid bad patterns:

- Python row loops over huge data
- `collect()` to driver
- converting huge data to pandas
- overusing Python UDFs

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| Python productivity | Python/JVM overhead |
| Spark scale | UDF performance pitfalls |
| DataFrame/SQL APIs | dependency packaging |
| broad ecosystem | debugging distributed Python errors |

## 11. Failure Modes

- Failure: Huge `toPandas()`.
- Symptom: driver OOM.
- Recovery: sample or write distributed output.
- Prevention: only convert small data.

- Failure: Python dependency missing on executors.
- Symptom: module import errors.
- Recovery: package dependencies correctly.
- Prevention: use cluster libraries or job packaging.

- Failure: Slow Python UDF.
- Symptom: poor performance.
- Recovery: replace with built-in/pandas UDF if appropriate.
- Prevention: prefer Spark SQL functions.

## 12. Common Mistakes

- Mistake: Thinking PySpark is pandas on big data.
- Why it is wrong: PySpark is distributed and lazy.
- Better approach: use Spark DataFrame operations.

- Mistake: Using normal Python lists/dicts for huge data.
- Why it is wrong: they live on driver.
- Better approach: keep data distributed.

## 13. Mini Example

Bad:

```python
rows = df.collect()
for row in rows:
    process(row)
```

Better:

```python
processed = df.withColumn("new_col", col("amount") * 2)
processed.write.parquet("/output")
```

## 14. Interview Questions

1. What is PySpark?
2. PySpark DataFrame vs pandas DataFrame?
3. Why is `collect()` dangerous?
4. Why can Python UDFs be slow?
5. How do you package dependencies for PySpark jobs?

## 15. Interview Speak

"PySpark is Spark's Python API. It lets Python users build distributed DataFrame and SQL transformations that execute on a Spark cluster. I use built-in Spark SQL functions where possible, avoid collecting large data to the driver, and treat PySpark as distributed lazy execution, not local pandas."

## 16. Quick Recall

- One-line summary: PySpark is Python code driving distributed Spark work.
- Three keywords: SparkSession, DataFrame, distributed.
- One trap: Treating PySpark like pandas.
- One memory trick: Python writes the instructions; Spark moves the heavy boxes.
