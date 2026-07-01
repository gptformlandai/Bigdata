# Topic 173: Fact And Dimension Tables

## 1. Goal

Understand the two core table types in dimensional analytics modeling.

## 2. Baby Intuition

Facts are what happened.

Dimensions describe the context around what happened.

Example:

```text
Fact: order amount = 100
Dimensions: customer, product, date, store
```

## 3. What It Is

- Simple definition: Fact tables store events/measures; dimension tables store descriptive attributes.
- Technical definition: A fact table records business process measurements at a defined grain and references dimension tables that provide descriptive context for filtering and grouping.
- Category: Dimensional modeling.
- Related terms: measure, metric, grain, foreign key, surrogate key, star schema.

## 4. Why It Exists

Business questions combine numbers and context:

```text
How much revenue by product category?
How many orders by customer segment?
What is churn by signup month?
```

Facts provide the numbers. Dimensions provide the grouping/filtering meaning.

## 5. Where It Fits In A Data Platform

```text
cleaned source data
  -> fact tables + dimension tables
  -> star schema marts
  -> BI dashboards
```

## 6. How It Works Step By Step

1. Choose business process, such as orders.
2. Define grain, such as one row per order line.
3. Create fact row for each event/transaction.
4. Store numeric measures in fact table.
5. Store descriptive attributes in dimension tables.
6. Link facts to dimensions using keys.
7. Query groups facts by dimension attributes.

## 7. How To Use It Practically

Fact table columns:

- foreign keys to dimensions
- measures
- degenerate identifiers if needed
- event timestamps

Dimension table columns:

- surrogate key
- business key
- names/descriptions
- categories
- hierarchy attributes
- SCD tracking fields if needed

## 8. Real-World Scenario

- Product/system: Food delivery analytics.
- Fact: delivery order.
- Measures: order_amount, delivery_fee, tip, delivery_duration.
- Dimensions: customer, restaurant, driver, city, date.
- What it enables: revenue by city, average delivery time by restaurant, tips by driver segment.

## 9. System Design Angle

Always clarify:

- What is the fact grain?
- What are the measures?
- What dimensions explain the measures?
- Are dimensions slowly changing?
- Are facts additive, semi-additive, or non-additive?

Fact types:

| Type | Example |
|---|---|
| transaction fact | one row per order |
| periodic snapshot | daily account balance |
| accumulating snapshot | order lifecycle from created to delivered |

## 10. Trade-offs

| Pros | Cons |
|---|---|
| clear analytics model | requires modeling effort |
| BI-friendly | grain mistakes cause bad metrics |
| reusable dimensions | SCD handling can be complex |
| consistent metrics | many-to-many relationships need care |

## 11. Failure Modes

- Failure: Fact grain not clear.
- Symptom: duplicate counts or wrong sums.
- Recovery: redesign/backfill fact.
- Prevention: document grain.

- Failure: Dimension key mismatch.
- Symptom: facts do not join to dimensions.
- Recovery: fix key mapping.
- Prevention: referential integrity checks.

- Failure: Current dimension used for history.
- Symptom: old sales appear under new region/category.
- Recovery: implement SCD Type 2 where needed.
- Prevention: define history behavior.

## 12. Common Mistakes

- Mistake: Calling every table a fact table.
- Why it is wrong: facts and dimensions serve different jobs.
- Better approach: identify event/measure tables vs descriptive context tables.

- Mistake: Mixing multiple grains in one fact.
- Why it is wrong: aggregates become incorrect.
- Better approach: one fact table should have one clear grain.

## 13. Mini Example

```text
fact_orders:
order_id, date_key, customer_key, product_key, quantity, revenue

dim_customer:
customer_key, customer_id, segment, signup_date, country
```

## 14. Interview Questions

1. Fact table vs dimension table?
2. What is grain?
3. What are measures?
4. What are surrogate keys?
5. What happens when dimension values change?

## 15. Interview Speak

"Fact tables store measurements at a specific grain, such as one row per order line. Dimension tables store descriptive context, such as customer, product, and date attributes. Correct grain and dimension history handling are critical for accurate analytics."

## 16. Quick Recall

- One-line summary: Facts are events/measures; dimensions describe them.
- Three keywords: grain, measures, context.
- One trap: Mixing grains.
- One memory trick: What happened plus around what.
