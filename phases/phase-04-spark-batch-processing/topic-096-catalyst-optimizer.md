# Topic 096: Catalyst Optimizer

## 1. Goal

Understand Catalyst as Spark SQL's query optimizer.

## 2. Baby Intuition

You give Spark a recipe.

Catalyst says:

```text
Can we do this recipe in a smarter order?
Can we skip ingredients?
Can we avoid extra work?
```

## 3. What It Is

- Simple definition: Catalyst optimizes Spark SQL/DataFrame plans.
- Technical definition: Catalyst is Spark SQL's extensible query optimizer that transforms parsed SQL/DataFrame operations into optimized logical and physical plans.
- Category: Query optimization engine.
- Related terms: logical plan, physical plan, rule-based optimization, cost-based optimization, projection pruning, predicate pushdown.

## 4. Why It Exists

Without an optimizer, Spark would execute code too literally.

Catalyst improves performance by:

- pushing filters closer to data
- selecting only required columns
- simplifying expressions
- reordering operations
- choosing join strategies
- pruning partitions

## 5. Where It Fits In A Data Platform

```text
SQL/DataFrame code -> Catalyst -> optimized plan -> Spark execution
```

Catalyst works with:

- Spark SQL
- DataFrame API
- many table/file sources

RDD code gets fewer Catalyst benefits because Spark cannot see inside arbitrary functions.

## 6. How It Works Step By Step

Query:

```sql
SELECT customer_id
FROM orders
WHERE dt = '2026-07-01' AND status = 'paid'
```

Catalyst flow:

1. Parse SQL into unresolved logical plan.
2. Analyze columns and tables using catalog.
3. Optimize logical plan.
4. Create physical plan candidates.
5. Choose physical plan.
6. Generate executable code.

Optimizations:

- read only `customer_id`, `dt`, `status`
- scan only `dt = 2026-07-01` partition
- push filter into file scan when possible

## 7. How To Use It Practically

Inspect plan:

```python
df.explain(True)
```

Look for:

- `PushedFilters`
- `PartitionFilters`
- `BroadcastHashJoin`
- `SortMergeJoin`
- `Exchange`
- `AdaptiveSparkPlan`

Help Catalyst:

- use DataFrames/Spark SQL
- avoid unnecessary UDFs
- use column expressions
- keep table statistics updated when applicable
- use efficient file formats

## 8. Real-World Scenario

- Product/system: Large Parquet analytics table.
- Problem: Query needs 5 columns out of 200.
- How Catalyst helps: Projection pruning reads only needed columns.
- What would go wrong without it: Spark might scan much more data.

## 9. System Design Angle

Catalyst matters because architecture is not just cluster size.

Bad query:

```text
scan everything, shuffle everything
```

Good optimized query:

```text
read needed partitions/columns, choose good join plan
```

This affects:

- runtime
- cloud cost
- cluster utilization
- user experience

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| automatic optimization | plans can be complex |
| better SQL/DataFrame speed | relies on visible expressions |
| join strategy choices | bad/missing stats can mislead |
| pruning/pushdown | UDFs can block optimization |

## 11. Failure Modes

- Failure: Python UDF hides logic.
- Symptom: optimizer cannot push/filter efficiently.
- Recovery: replace with built-in functions.
- Prevention: prefer SQL functions.

- Failure: Bad stats.
- Symptom: poor join strategy.
- Recovery: analyze/update stats or hint.
- Prevention: maintain table metadata.

## 12. Common Mistakes

- Mistake: Using RDDs for structured work.
- Why it is wrong: Catalyst cannot optimize opaque RDD logic.
- Better approach: use DataFrames/Spark SQL.

- Mistake: Never reading explain plans.
- Why it is wrong: you miss scans, exchanges, bad joins.
- Better approach: inspect physical plans.

## 13. Mini Example

Before optimization:

```text
read all columns -> filter -> select customer_id
```

After optimization:

```text
read only needed columns and partitions -> filter -> output
```

## 14. Interview Questions

1. What is Catalyst?
2. What optimizations does Catalyst perform?
3. Why are DataFrames easier to optimize than RDDs?
4. How do UDFs affect Catalyst?
5. What do you look for in `explain()`?

## 15. Interview Speak

"Catalyst is Spark SQL's optimizer. It transforms SQL/DataFrame plans through analysis, logical optimization, and physical planning. It enables optimizations like predicate pushdown, projection pruning, partition pruning, and join strategy selection. To help Catalyst, I prefer built-in column expressions over opaque UDFs."

## 16. Quick Recall

- One-line summary: Catalyst makes Spark SQL/DataFrames smarter before execution.
- Three keywords: logical plan, physical plan, pruning.
- One trap: Hiding logic inside UDFs.
- One memory trick: Catalyst is Spark's query planner brain.
