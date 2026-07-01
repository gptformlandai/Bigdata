# Topic 071: Bucketing In Hive

## 1. Goal

Understand Hive bucketing as a way to organize rows into a fixed number of files based on a hash of a column.

## 2. Baby Intuition

Partitioning is like separating students by grade.

Bucketing is like assigning students within a grade into numbered classrooms using a rule.

The number of classrooms is fixed.

## 3. What It Is

- Simple definition: Bucketing splits table data into a fixed number of buckets using a hash of one or more columns.
- Technical definition: Hive bucketing clusters rows into bucket files by applying a hash function to bucketing columns and assigning rows to a configured number of buckets.
- Category: Data layout optimization.
- Related terms: bucket column, bucket count, hash, sort, join optimization, sampling.

## 4. Why It Exists

Partitioning alone can be too coarse or too many.

Example:

```text
Partition by date -> good
Partition by user_id -> too many partitions
```

Bucketing gives another option:

```text
Within each date, distribute users into 64 bucket files.
```

This can help with:

- joins
- sampling
- predictable file organization
- reducing shuffle when bucketed tables align

## 5. Where It Fits In A Data Platform

```text
Hive table -> partitions -> bucket files
```

Example layout:

```text
orders/dt=2026-07-01/bucket_00000
orders/dt=2026-07-01/bucket_00001
orders/dt=2026-07-01/bucket_00002
```

Partitioning chooses folders.

Bucketing chooses files inside folders.

## 6. How It Works Step By Step

Table definition:

```sql
CREATE TABLE orders_bucketed (
    order_id STRING,
    customer_id STRING,
    amount DOUBLE
)
PARTITIONED BY (dt STRING)
CLUSTERED BY (customer_id) INTO 32 BUCKETS
STORED AS ORC;
```

Write flow:

1. Hive reads each row.
2. It hashes `customer_id`.
3. It computes bucket number.
4. It writes row to that bucket file.

Mental formula:

```text
bucket = hash(customer_id) % number_of_buckets
```

## 7. How To Use It Practically

Create bucketed table:

```sql
CREATE TABLE user_events_bucketed (
    user_id STRING,
    event_type STRING
)
CLUSTERED BY (user_id) INTO 64 BUCKETS
STORED AS ORC;
```

Sample from bucket:

```sql
SELECT *
FROM user_events_bucketed
TABLESAMPLE(BUCKET 1 OUT OF 64 ON user_id);
```

Practical note:

```text
Bucketing only helps when data is actually written respecting bucket rules.
```

## 8. Real-World Scenario

- Product/system: Large order analytics.
- Problem: Orders and customer events are frequently joined by `customer_id`.
- How bucketing helps: If both tables are bucketed by `customer_id` with compatible bucket counts, joins may be more efficient.
- What would go wrong without it: The engine may need a large shuffle to group matching customers.

## 9. System Design Angle

Bucketing can help when:

- joins happen often on the same key
- sampling is needed
- partitioning by the key would create too many partitions
- data layout can be controlled during writes

Bucketing is less useful when:

- query engine ignores bucket metadata
- bucket count is badly chosen
- data is written incorrectly
- join keys vary widely

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| better join layout | write-time complexity |
| fixed number of files | bucket count planning |
| sampling support | engine compatibility dependency |
| avoids high-cardinality partitions | can still have skew |

## 11. Failure Modes

- Failure: Skewed bucket key.
- Symptom: one bucket much larger than others.
- Recovery: choose better key or add salting.
- Prevention: inspect key distribution.

- Failure: Wrong bucket count.
- Symptom: too many small files or too little parallelism.
- Recovery: rewrite table with better bucket count.
- Prevention: size buckets based on data volume and query engine.

- Failure: Engine does not use bucketing.
- Symptom: no performance benefit.
- Recovery: verify execution plan.
- Prevention: understand engine support.

## 12. Common Mistakes

- Mistake: Confusing partitioning and bucketing.
- Why it is wrong: partitioning creates folders by value; bucketing creates fixed files by hash.
- Better approach: use partitioning for pruning and bucketing for join/layout benefits.

- Mistake: Bucketing tiny tables.
- Why it is wrong: adds complexity without benefit.
- Better approach: use bucketing for large tables with repeated join patterns.

## 13. Mini Example

If there are 4 buckets:

```text
hash(customer_id) % 4
```

Rows go to:

```text
bucket 0
bucket 1
bucket 2
bucket 3
```

The number of buckets is fixed even if customer count grows.

## 14. Interview Questions

1. What is bucketing in Hive?
2. How is bucketing different from partitioning?
3. When can bucketing improve joins?
4. What happens if bucket key is skewed?
5. Why must data be written according to bucket rules?

## 15. Interview Speak

"Hive bucketing distributes rows into a fixed number of files using a hash of a bucket column. Partitioning helps skip folders, while bucketing helps organize rows within partitions and can improve joins or sampling when query engines use the bucket metadata."

## 16. Quick Recall

- One-line summary: Bucketing hashes rows into a fixed number of files.
- Three keywords: hash, buckets, joins.
- One trap: Confusing buckets with partitions.
- One memory trick: Partition is a shelf; bucket is a numbered box on the shelf.
