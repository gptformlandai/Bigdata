# Topic 097: Tungsten Engine

## 1. Goal

Understand Tungsten as Spark's low-level execution optimization project.

## 2. Baby Intuition

Catalyst decides the smart plan.

Tungsten helps execute that plan efficiently by caring about memory, CPU, and binary data layout.

If Catalyst is the planner, Tungsten is the performance mechanic.

## 3. What It Is

- Simple definition: Tungsten improves Spark's runtime performance.
- Technical definition: Tungsten is Spark's execution engine optimization effort focused on memory management, cache-friendly binary processing, whole-stage code generation, and CPU efficiency.
- Category: Spark execution internals.
- Related terms: off-heap memory, binary format, whole-stage codegen, UnsafeRow, CPU cache.

## 4. Why It Exists

Distributed processing is not only about many machines.

Each machine must use CPU and memory efficiently.

Older object-heavy execution created overhead from:

- JVM objects
- garbage collection
- serialization
- poor CPU cache usage

Tungsten exists to reduce those costs.

## 5. Where It Fits In A Data Platform

```text
Spark SQL/DataFrame physical plan -> Tungsten execution -> efficient CPU/memory use
```

You usually do not call Tungsten directly.

You benefit from it by using Spark SQL/DataFrames and built-in functions.

## 6. How It Works Step By Step

Tungsten improves execution through:

1. Binary memory format instead of many JVM objects.
2. Better memory management.
3. Whole-stage code generation.
4. Reduced virtual function calls.
5. More CPU-cache-friendly processing.

Whole-stage code generation means Spark can generate optimized Java bytecode for a pipeline of operators.

## 7. How To Use It Practically

You do not write:

```text
use Tungsten
```

Instead:

- use DataFrames/Spark SQL
- use built-in functions
- avoid Python UDFs when possible
- inspect physical plan for codegen markers

In `explain()` you may see:

```text
*(1) Project
*(1) Filter
```

The `*` indicates whole-stage codegen participation in many Spark plans.

## 8. Real-World Scenario

- Product/system: Large ETL with many column expressions.
- Problem: Need efficient CPU execution over billions of rows.
- How Tungsten helps: Reduces object overhead and generates efficient execution code.
- What would go wrong without it: More JVM overhead, GC pressure, and slower processing.

## 9. System Design Angle

Tungsten is not usually a design component, but it affects API choice.

If you use:

- DataFrame expressions
- Spark SQL built-ins

Spark can optimize execution better.

If you use:

- Python UDFs
- arbitrary row-by-row logic

You may bypass some optimizations.

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| faster execution | more complex internals |
| lower JVM overhead | less transparent debugging |
| better memory layout | benefits depend on API usage |
| code generation | generated code can be hard to inspect |

## 11. Failure Modes

- Failure: Codegen disabled/falls back.
- Symptom: slower execution.
- Recovery: inspect plan and simplify expressions.
- Prevention: use supported built-ins.

- Failure: Memory pressure still high.
- Symptom: spill/OOM.
- Recovery: tune partitions/memory.
- Prevention: avoid huge rows and skew.

## 12. Common Mistakes

- Mistake: Thinking Tungsten means no memory issues.
- Why it is wrong: it optimizes memory use, but bad jobs can still OOM.
- Better approach: still tune partitions, joins, cache, and skew.

- Mistake: Using UDFs for simple expressions.
- Why it is wrong: may lose codegen/optimizer benefits.
- Better approach: use built-in functions.

## 13. Mini Example

Better:

```python
from pyspark.sql.functions import col

df.withColumn("net", col("amount") - col("discount"))
```

Worse for optimization:

```python
udf(lambda amount, discount: amount - discount)
```

## 14. Interview Questions

1. What is Tungsten?
2. How is Tungsten different from Catalyst?
3. What is whole-stage code generation?
4. Why do built-in functions help performance?
5. Does Tungsten remove memory tuning?

## 15. Interview Speak

"Tungsten is Spark's execution optimization layer focused on CPU and memory efficiency, including binary memory format and whole-stage code generation. Catalyst chooses an optimized plan, while Tungsten helps execute it efficiently. Using DataFrames and built-in SQL functions helps Spark benefit from these optimizations."

## 16. Quick Recall

- One-line summary: Tungsten makes Spark execution CPU/memory efficient.
- Three keywords: codegen, binary, memory.
- One trap: Thinking it fixes all OOMs.
- One memory trick: Catalyst plans; Tungsten accelerates.
