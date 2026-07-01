# Topic 172: Snowflake Schema

## 1. Goal

Understand snowflake schema as a more normalized version of star schema.

## 2. Baby Intuition

Star schema keeps dimension details in one wide table.

Snowflake schema splits dimension details into smaller related tables, like branches from a branch.

## 3. What It Is

- Simple definition: Snowflake schema normalizes dimension tables into multiple related tables.
- Technical definition: A snowflake schema is a dimensional model where dimensions are normalized into sub-dimensions, reducing redundancy but increasing joins.
- Category: Dimensional data modeling.
- Related terms: star schema, normalization, dimension, hierarchy, fact table, BI.

## 4. Why It Exists

Sometimes dimensions have hierarchy:

```text
product -> category -> department
city -> state -> country
store -> region -> division
```

Snowflake schema separates these hierarchy levels to reduce duplication and enforce consistency.

## 5. Where It Fits In A Data Platform

```text
fact_sales
  -> dim_product
      -> dim_category
          -> dim_department
```

It appears in warehouses where dimension data is complex or needs normalized management.

## 6. How It Works Step By Step

1. Fact table stores measures and keys.
2. Fact joins to a dimension table.
3. Dimension table joins to sub-dimension tables.
4. Queries may need more joins to reach attributes.
5. Storage duplication is reduced.

## 7. How To Use It Practically

Star version:

```text
dim_product(product_key, product_name, category_name, department_name)
```

Snowflake version:

```text
dim_product(product_key, product_name, category_key)
dim_category(category_key, category_name, department_key)
dim_department(department_key, department_name)
```

## 8. Real-World Scenario

- Product/system: Global store reporting.
- Problem: location hierarchy is reused across many dimensions and needs central management.
- How snowflake schema helps: city/state/country hierarchy can be normalized and reused.
- What would go wrong without it: duplicated hierarchy values can drift.

## 9. System Design Angle

Use snowflake schema when:

- dimensions are large/complex
- hierarchies need central management
- duplication is costly
- data governance favors normalized dimensions

Prefer star schema when:

- BI simplicity matters more
- query speed and fewer joins matter
- dimensions are not too large

## 10. Trade-offs

| Pros | Cons |
|---|---|
| less duplication | more joins |
| cleaner hierarchies | harder for analysts |
| consistency in sub-dimensions | BI queries can be slower/complex |
| normalized management | less simple than star schema |

## 11. Failure Modes

- Failure: Too many normalized tables.
- Symptom: analysts struggle with joins.
- Recovery: create flattened marts/views.
- Prevention: normalize only where it adds value.

- Failure: Join path confusion.
- Symptom: wrong reports.
- Recovery: semantic layer.
- Prevention: clear model docs.

- Failure: Performance degradation.
- Symptom: dashboard joins many dimensions repeatedly.
- Recovery: denormalize/aggregate.
- Prevention: model for query patterns.

## 12. Common Mistakes

- Mistake: Choosing snowflake schema just because it sounds advanced.
- Why it is wrong: simpler star schema is often better for BI.
- Better approach: normalize only for real hierarchy/duplication needs.

- Mistake: Exposing complex snowflake joins to every analyst.
- Why it is wrong: it increases query mistakes.
- Better approach: create user-friendly views or marts.

## 13. Mini Example

```text
Star:
fact_sales -> dim_product

Snowflake:
fact_sales -> dim_product -> dim_category -> dim_department
```

## 14. Interview Questions

1. What is snowflake schema?
2. Star schema vs snowflake schema?
3. Why normalize dimensions?
4. What is the performance trade-off?
5. Which one is easier for BI users?

## 15. Interview Speak

"A snowflake schema normalizes dimensions into sub-dimensions, reducing duplication and managing hierarchies more cleanly. The trade-off is more joins and more complexity, so for BI I often prefer star schema unless the dimension hierarchy or governance need justifies snowflaking."

## 16. Quick Recall

- One-line summary: Snowflake schema normalizes dimensions into branches.
- Three keywords: normalized, hierarchy, joins.
- One trap: Making BI models too complex.
- One memory trick: Star rays grow branches.
