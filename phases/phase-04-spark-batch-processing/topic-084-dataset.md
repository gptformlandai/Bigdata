# Topic 084: Dataset

## 1. Goal

Understand Dataset as Spark's typed structured API, mostly important in Scala/Java.

## 2. Baby Intuition

A DataFrame is like a table where Spark knows column names and types at runtime.

A Dataset is like a table where your programming language also knows the record type more strongly.

## 3. What It Is

- Simple definition: Dataset is a typed distributed collection in Spark.
- Technical definition: A Dataset is a strongly typed distributed collection that combines RDD-like type safety with Spark SQL optimization, primarily used in Scala and Java.
- Category: Structured Spark API.
- Related terms: DataFrame, encoder, case class, type safety, Spark SQL.

## 4. Why It Exists

Spark wanted an API that gives:

- structured optimization like DataFrames
- compile-time type safety like strongly typed languages
- object-oriented transformations

This matters more in Scala/Java than Python.

In PySpark, DataFrame is the main API. Python does not use typed Datasets the same way.

## 5. Where It Fits In A Data Platform

```text
Structured data -> Dataset transformations -> optimized Spark execution
```

Used mainly by:

- Scala Spark teams
- Java Spark teams
- strongly typed ETL codebases

Less relevant for:

- PySpark-only learners
- SQL-only pipelines

## 6. How It Works Step By Step

Scala idea:

```scala
case class Order(orderId: String, customerId: String, amount: Double)

val orders: Dataset[Order] = spark.read.parquet("/data/orders").as[Order]
```

Spark knows:

- distributed data plan
- schema
- typed object shape through encoders

## 7. How To Use It Practically

Scala example:

```scala
case class Order(orderId: String, customerId: String, amount: Double, status: String)

val orders = spark.read.parquet("/data/orders").as[Order]

val paid = orders.filter(order => order.status == "paid")
```

PySpark note:

```text
In Python, use DataFrames. Dataset API is not the normal PySpark path.
```

## 8. Real-World Scenario

- Product/system: Scala-based ETL platform.
- Problem: Team wants type safety for domain records.
- How Dataset helps: Compile-time checks catch some field/type mistakes earlier.
- What would go wrong without it: More errors may appear only at runtime.

## 9. System Design Angle

Dataset is not usually the main architecture decision.

The bigger decisions are:

- Spark vs warehouse
- DataFrame vs RDD
- batch vs streaming
- storage format
- partitioning
- join strategy

Dataset is a language/API choice, mainly for typed JVM code.

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| type safety in Scala/Java | less relevant in Python |
| structured optimization | encoder overhead/complexity |
| object-oriented API | sometimes less concise than SQL |
| compile-time checks | still must understand distributed execution |

## 11. Failure Modes

- Failure: Encoder/schema mismatch.
- Symptom: runtime conversion errors.
- Recovery: fix schema or case class.
- Prevention: schema validation.

- Failure: Overusing object functions.
- Symptom: optimizer has less visibility.
- Recovery: use DataFrame/Spark SQL expressions.
- Prevention: prefer columnar expressions for performance-critical logic.

## 12. Common Mistakes

- Mistake: Thinking Dataset is required for PySpark.
- Why it is wrong: PySpark uses DataFrames.
- Better approach: learn Dataset conceptually, focus on DataFrame for Python.

- Mistake: Thinking type safety solves data quality.
- Why it is wrong: bad values can still exist.
- Better approach: combine type safety with validation.

## 13. Mini Example

DataFrame:

```text
table-like rows and columns
```

Dataset:

```text
typed records, like Dataset[Order] in Scala
```

## 14. Interview Questions

1. What is a Dataset?
2. How is Dataset different from DataFrame?
3. Why is Dataset mostly relevant in Scala/Java?
4. What are encoders?
5. Should PySpark users focus on Dataset?

## 15. Interview Speak

"A Dataset is Spark's typed structured API, mainly used in Scala and Java. It combines DataFrame-style optimization with stronger compile-time type safety. In PySpark, the DataFrame API is the standard path, so Dataset is usually more conceptual unless working in JVM languages."

## 16. Quick Recall

- One-line summary: Dataset is a typed Spark structured API.
- Three keywords: typed, Scala, encoder.
- One trap: Thinking PySpark requires Datasets.
- One memory trick: DataFrame is table; Dataset is typed table in Scala/Java.
