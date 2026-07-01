# Topic 276: SQL Interview Questions

## 1. Goal

Prepare for SQL interviews focused on analytics, joins, windows, deduplication, ranking, and query reasoning.

## 2. Baby Intuition

SQL interviews test how you think with tables.

You need to read the question, identify the grain, join correctly, aggregate correctly, and avoid double-counting.

## 3. Must-Know SQL Areas

- joins
- grouping and aggregation
- window functions
- CTEs
- subqueries
- deduplication
- ranking
- date/time logic
- null handling
- query performance
- slowly changing dimensions

## 4. Basic Questions

| Question | Key Idea |
|---|---|
| inner vs left join | inner keeps matches, left keeps all left rows |
| where vs having | where filters rows before group, having filters groups |
| count(*) vs count(column) | count(column) ignores nulls |
| union vs union all | union removes duplicates, union all keeps all |
| primary key vs foreign key | uniqueness vs relationship |

## 5. Window Function Questions

Common patterns:

```sql
row_number() over (partition by user_id order by event_time desc)
rank() over (partition by category order by revenue desc)
sum(amount) over (partition by user_id order by event_time)
```

Use windows when you need row-level output plus group-level context.

Examples:

- latest record per user
- top N products per category
- running total
- session gap detection
- dedupe

## 6. Deduplication Pattern

Question:

```text
Get the latest event per user.
```

Pattern:

```sql
with ranked as (
  select
    user_id,
    event_time,
    event_type,
    row_number() over (
      partition by user_id
      order by event_time desc
    ) as rn
  from events
)
select *
from ranked
where rn = 1;
```

## 7. Funnel Pattern

Question:

```text
How many users viewed product, added to cart, and purchased?
```

Think:

- one row per user/session
- conditional aggregation
- preserve event order if required

Simple pattern:

```sql
select
  count(distinct case when event_type = 'view' then user_id end) as viewers,
  count(distinct case when event_type = 'cart' then user_id end) as cart_users,
  count(distinct case when event_type = 'purchase' then user_id end) as purchasers
from events
where event_date = date '2026-07-02';
```

## 8. SCD Type 2 Join Pattern

Question:

```text
Join facts to the customer dimension as of transaction date.
```

Pattern:

```sql
select
  f.order_id,
  f.order_date,
  d.customer_segment
from fact_orders f
join dim_customer d
  on f.customer_id = d.customer_id
 and f.order_date >= d.valid_from
 and f.order_date < coalesce(d.valid_to, date '9999-12-31');
```

## 9. Performance Questions

When a SQL query is slow, check:

- scans too much data
- missing partition filter
- unnecessary columns
- join order
- exploding joins
- high-cardinality group by
- no clustering/sort benefit
- repeated subqueries

Strong line:

```text
I first check the query plan and data scanned before rewriting blindly.
```

## 10. Common Mistakes

| Mistake | Better Approach |
|---|---|
| not knowing table grain | identify one row means what |
| joining facts before aggregating | avoid row explosion |
| count instead of count distinct | choose based on metric definition |
| ignoring nulls | handle null intentionally |
| no date filter | always bound large analytics queries |

## 11. Practice Questions

1. Find the second highest salary by department.
2. Find users active on 3 consecutive days.
3. Deduplicate events by latest event_time.
4. Calculate 7-day rolling revenue.
5. Find top 3 products by category.
6. Join orders to SCD customer dimension.
7. Calculate conversion funnel.
8. Identify customers who bought product A but not B.

## 12. Interview Speak

"Before writing SQL, I identify the grain of each table and the target output grain. Then I decide the join path, filters, grouping, and whether a window function is needed. I also watch for duplicate rows, nulls, and whether the metric requires count or count distinct."

## 13. Quick Recall

- One-line summary: SQL interviews are about grain, joins, aggregation, and windows.
- Three keywords: grain, window, dedupe.
- One trap: double-counting after a join.
- Memory trick: know the row before counting the rows.

