# Topic 277: Data Modeling Interview Questions

## 1. Goal

Prepare for data modeling interviews around facts, dimensions, grain, slowly changing dimensions, and analytics-ready tables.

## 2. Baby Intuition

Data modeling is arranging data so business questions are easy and correct.

Bad modeling makes every query painful. Good modeling makes common questions simple.

## 3. Must-Know Concepts

- fact table
- dimension table
- grain
- star schema
- snowflake schema
- slowly changing dimensions
- factless fact
- snapshot fact
- accumulating snapshot
- bridge table
- data mart

## 4. First Question To Ask

Always ask:

```text
What is the grain?
```

Examples:

- one row per order
- one row per order item
- one row per user per day
- one row per transaction
- one row per account per month

If grain is unclear, metrics become wrong.

## 5. Fact Vs Dimension

| Table Type | Meaning | Examples |
|---|---|---|
| fact | measurable business event | order, payment, page view |
| dimension | descriptive context | customer, product, date, store |

Fact columns:

- keys to dimensions
- measures like amount, quantity, duration
- event date/time

Dimension columns:

- descriptive attributes
- hierarchy
- effective dates if SCD

## 6. Star Vs Snowflake

Star schema:

- central fact table
- denormalized dimensions
- easier for BI

Snowflake schema:

- normalized dimensions
- less duplication
- more joins

Interview line:

```text
For analytics, I usually start with star schema because it is simpler and faster for BI users.
```

## 7. Slowly Changing Dimensions

| Type | Meaning | Example |
|---|---|---|
| Type 1 | overwrite old value | fix typo in customer name |
| Type 2 | keep history with valid_from/valid_to | customer segment changed |
| Type 3 | keep limited previous value | previous region |

SCD Type 2 is important when historical reporting must reflect old attribute values.

## 8. Common Modeling Prompts

| Prompt | Model |
|---|---|
| e-commerce orders | fact_order_item + dim_customer + dim_product + dim_date |
| subscriptions | fact_subscription_event + snapshot active subscriptions |
| ad analytics | fact_impression, fact_click, fact_conversion |
| finance reporting | invoice/payment facts, fiscal date dimension, SCD customer |
| user activity | daily user activity fact |

## 9. Many-To-Many Handling

Problem:

```text
one order can have many promotions
one promotion can apply to many orders
```

Use bridge table:

```text
bridge_order_promotion(order_id, promotion_id, allocation_percent)
```

This prevents messy duplicated metrics.

## 10. Late Arriving Data

Late facts:

- event arrives after reporting period
- update/restate affected aggregate

Late dimensions:

- fact arrives before dimension row
- use unknown dimension key temporarily
- update when dimension arrives

## 11. Common Mistakes

| Mistake | Better Approach |
|---|---|
| no declared grain | write grain at top of model |
| mixing facts and dimensions | keep events/measures separate from descriptors |
| ignoring SCD | choose Type 1/2 based on reporting need |
| dimensions too normalized for BI | denormalize when simplicity matters |
| duplicate facts from many-to-many joins | use bridge/allocation |

## 12. Practice Questions

1. Model an e-commerce warehouse.
2. Model Netflix viewing analytics.
3. Model ad impressions/clicks/conversions.
4. Model a finance revenue mart.
5. Explain SCD Type 2.
6. What is a snapshot fact table?
7. How do you avoid double-counting?
8. How do you model many-to-many relationships?

## 13. Interview Speak

"I start by clarifying the business process and the grain. Then I identify facts, dimensions, keys, measures, and historical tracking needs. For BI, I prefer star schemas with certified facts and conformed dimensions. If attributes change over time, I choose SCD Type 1 or Type 2 based on whether historical reporting must preserve old values."

## 14. Quick Recall

- One-line summary: Data modeling makes business metrics easy and correct.
- Three keywords: grain, fact, dimension.
- One trap: unclear grain.
- Memory trick: first define one row.

