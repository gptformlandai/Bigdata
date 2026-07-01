# Topic 171: Star Schema

## 1. Goal

Understand star schema as a simple analytics modeling pattern using one central fact table and surrounding dimensions.

## 2. Baby Intuition

A star schema looks like a star.

The fact table is in the middle, and dimension tables point into it like rays.

## 3. What It Is

- Simple definition: Star schema is a warehouse model with a central fact table connected to dimension tables.
- Technical definition: A star schema organizes analytical data into denormalized dimension tables joined directly to a central fact table containing measures and foreign keys.
- Category: Dimensional data modeling.
- Related terms: fact table, dimension table, surrogate key, measure, grain, BI, OLAP.

## 4. Why It Exists

Business analytics needs tables that are:

- easy to understand
- fast to query
- friendly to BI tools
- consistent for metrics
- simpler than normalized OLTP schemas

Star schema makes analytics easier by separating measurable events from descriptive context.

## 5. Where It Fits In A Data Platform

```text
cleaned warehouse tables
  -> star schema marts
  -> BI dashboards and analysts
```

Example:

```text
fact_orders
  -> dim_customer
  -> dim_product
  -> dim_date
  -> dim_store
```

## 6. How It Works Step By Step

1. Define the business process, such as orders.
2. Define the grain, such as one row per order line.
3. Create fact table with measures and foreign keys.
4. Create dimension tables with descriptive attributes.
5. Analysts join facts to dimensions for slicing metrics.
6. BI tools use the model for dashboards.

## 7. How To Use It Practically

Fact table example:

```text
fact_order_line
order_line_id, order_date_key, customer_key, product_key, quantity, revenue
```

Dimension example:

```text
dim_product
product_key, product_id, product_name, category, brand
```

Important word:

```text
grain = what one row means
```

## 8. Real-World Scenario

- Product/system: Sales reporting mart.
- Problem: Business wants revenue by date, product, customer segment, and store.
- How star schema helps: fact_sales joins directly to clear dimensions.
- What would go wrong without it: users struggle through normalized source tables and inconsistent joins.

## 9. System Design Angle

Mention star schema when:

- BI/reporting is required
- metrics need dimensions
- warehouse marts are needed
- business users need easy SQL
- dashboards repeat common joins

Design order:

```text
business process -> grain -> dimensions -> facts -> measures
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| easy for analysts | dimension duplication |
| BI-friendly | denormalization maintenance |
| simpler joins | may not model every relationship elegantly |
| good query performance | fact grain mistakes are costly |

## 11. Failure Modes

- Failure: Wrong grain.
- Symptom: double-counting or missing metrics.
- Recovery: rebuild fact table.
- Prevention: define grain before columns.

- Failure: Many-to-many dimension joins.
- Symptom: duplicated facts.
- Recovery: bridge table or model redesign.
- Prevention: understand relationships.

- Failure: Slowly changing dimensions ignored.
- Symptom: historical reports use current attributes incorrectly.
- Recovery: SCD design.
- Prevention: decide history behavior per dimension.

## 12. Common Mistakes

- Mistake: Starting with columns before grain.
- Why it is wrong: row meaning becomes unclear.
- Better approach: define one row's meaning first.

- Mistake: Putting descriptive attributes in facts.
- Why it is wrong: facts become wide and inconsistent.
- Better approach: place descriptions in dimensions.

## 13. Mini Example

```text
Question:
Revenue by product category by month

Query:
fact_sales joins dim_product and dim_date
then groups by category and month
```

## 14. Interview Questions

1. What is a star schema?
2. What is a fact table?
3. What is a dimension table?
4. What is grain?
5. Why is star schema BI-friendly?

## 15. Interview Speak

"A star schema models analytics around a central fact table and surrounding dimensions. The first design decision is the grain of the fact table. Facts hold measures and keys, while dimensions hold descriptive attributes used for filtering, grouping, and reporting."

## 16. Quick Recall

- One-line summary: Star schema is fact table in center, dimensions around it.
- Three keywords: fact, dimension, grain.
- One trap: Wrong grain causes wrong metrics.
- One memory trick: Fact sun, dimension rays.
