# Topic 099: Data Skew

## 1. Goal

Understand data skew as uneven data distribution that causes slow Spark tasks.

## 2. Baby Intuition

Imagine 10 workers packing boxes.

Nine workers get 10 boxes each. One worker gets 10,000 boxes.

The whole job waits for that one overloaded worker.

That is skew.

## 3. What It Is

- Simple definition: Data skew means some partitions or keys have much more data than others.
- Technical definition: Data skew occurs when data distribution across partitions or keys is uneven, causing a small number of tasks to process disproportionately large data.
- Category: Performance bottleneck.
- Related terms: hot key, straggler task, shuffle skew, salting, AQE.

## 4. Why It Exists

Real data is rarely uniform.

Examples:

- one customer has millions of orders
- one country has most users
- null key appears in many rows
- one campaign receives huge traffic
- one date/hour has special event traffic

Spark parallelism depends on balanced partitions. Skew breaks that balance.

## 5. Where It Fits In A Data Platform

```text
groupBy/join/repartition -> shuffle by key -> skewed partitions -> slow tasks
```

Skew is common in:

- joins
- aggregations
- deduplication
- window functions
- repartition by key

## 6. How It Works Step By Step

Example:

```python
events.groupBy("country").count()
```

If 80 percent of rows are `country = 'US'`:

1. Spark shuffles by country.
2. Most rows for `US` go to one reducer partition.
3. That task becomes huge.
4. Other tasks finish quickly.
5. Stage waits for the US task.

## 7. How To Use It Practically

Detect skew:

- Spark UI shows one/few tasks much slower.
- Task input sizes vary a lot.
- Shuffle read size is uneven.
- Stage stuck near 99 percent.

Check key distribution:

```python
df.groupBy("key").count().orderBy("count", ascending=False).show(20)
```

Mitigations:

- salting hot keys
- broadcast join small table
- AQE skew join
- pre-aggregate
- filter nulls separately
- choose better partition key

## 8. Real-World Scenario

- Product/system: Global usage analytics.
- Problem: Most events are from one country.
- How skew appears: groupBy country creates one huge reducer task.
- What would go wrong without fixing it: one task delays the whole job or OOMs.

## 9. System Design Angle

Skew affects:

- runtime
- executor memory
- shuffle spill
- job reliability
- cost

In interviews, always mention skew when discussing:

- partitioning
- joins
- groupBy
- hot keys
- uneven tenants

## 10. Trade-offs

| What We Gain By Fixing Skew | What We Pay |
|---|---|
| faster stages | more complex logic |
| fewer OOMs | salting requires cleanup |
| better cluster utilization | extra shuffle sometimes |
| reliable jobs | more data profiling |

## 11. Failure Modes

- Failure: Hot key join.
- Symptom: one task huge, executor OOM.
- Recovery: salt key or use AQE skew join.
- Prevention: profile join key distribution.

- Failure: Null key skew.
- Symptom: all nulls go to same partition.
- Recovery: handle nulls separately.
- Prevention: clean keys before shuffle.

## 12. Common Mistakes

- Mistake: Adding more executors to fix skew.
- Why it is wrong: hot key may still go to one task.
- Better approach: fix distribution.

- Mistake: Repartitioning by a skewed key.
- Why it is wrong: creates hot partition.
- Better approach: choose better key or salt.

## 13. Mini Example

Salting idea:

```text
hot key: customer_1

salted keys:
customer_1#0
customer_1#1
customer_1#2
customer_1#3
```

Spread hot key across multiple partitions, then combine later.

## 14. Interview Questions

1. What is data skew?
2. How do you detect skew in Spark?
3. Why does skew hurt joins?
4. What is salting?
5. Why does adding executors not always fix skew?

## 15. Interview Speak

"Data skew means some keys or partitions are much larger than others, so a few tasks become stragglers. I detect it in Spark UI through uneven task durations and shuffle sizes, then fix it with salting, AQE skew join handling, pre-aggregation, better partition keys, or special handling for hot/null keys."

## 16. Quick Recall

- One-line summary: Skew means one task gets too much work.
- Three keywords: hot key, straggler, salting.
- One trap: Adding executors without fixing the hot key.
- One memory trick: One worker gets all the boxes.
