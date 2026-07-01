# Topic 238: Medallion Architecture

## 1. Goal

Understand Medallion architecture as a layered lakehouse design pattern.

## 2. Baby Intuition

Medallion architecture is like cleaning raw ingredients into a prepared meal.

Bronze stores raw ingredients, silver cleans them, and gold serves business-ready dishes.

## 3. What It Is

- Simple definition: Medallion architecture organizes data into bronze, silver, and gold layers.
- Technical definition: Medallion architecture is a lakehouse pattern that progressively improves data quality and business usability through raw, cleaned, and curated layers.
- Category: Lakehouse data organization pattern.
- Related terms: bronze, silver, gold, data quality, lakehouse, Delta, Iceberg, curated data.

## 4. Why It Exists

Data arrives messy:

- duplicates
- missing fields
- schema drift
- bad records
- late events
- raw business codes

Putting everything directly into final dashboards creates chaos.

Medallion architecture gives a repeatable path from raw data to trusted data.

## 5. Where It Fits In A Data Platform

```text
sources
  -> bronze raw tables
  -> silver cleaned/conformed tables
  -> gold business marts/aggregates
  -> BI/ML/products
```

## 6. How It Works Step By Step

1. Bronze ingests source data with minimal changes.
2. Silver validates, deduplicates, casts, standardizes, and joins.
3. Gold creates business-ready aggregates, facts, dimensions, and metrics.
4. Quality checks run between layers.
5. Lineage connects sources to outputs.
6. Users consume mostly silver/gold, not raw bronze.

## 7. How To Use It Practically

Layer meaning:

| Layer | Purpose | Consumers |
|---|---|---|
| bronze | raw replayable data | data engineers |
| silver | cleaned reliable data | engineers, analysts, ML |
| gold | business-ready metrics | BI, product, executives |

Good practices:

- keep bronze immutable when possible
- document transformations
- apply quality gates
- restrict raw sensitive data
- make gold definitions governed

## 8. Real-World Scenario

- Product/system: Retail lakehouse.
- Problem: Orders, payments, and click events arrive from many systems.
- How medallion helps: bronze stores raw events, silver cleans/dedupes, gold builds revenue and conversion metrics.
- What would go wrong without it: dashboards query raw inconsistent data.

## 9. System Design Angle

Use medallion architecture when:

- building a lakehouse
- many sources feed analytics
- quality improves in stages
- raw replay and business marts both matter

Key phrase:

```text
Bronze is for replay, silver is for reliability, gold is for business consumption.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| clear data maturity levels | more storage copies |
| replayable raw data | more pipeline stages |
| quality gates | latency between layers |
| business-friendly gold | governance required |

## 11. Failure Modes

- Failure: Gold built directly from raw.
- Symptom: dashboard instability.
- Recovery: introduce silver cleanup.
- Prevention: layer standards.

- Failure: Bronze not replayable.
- Symptom: cannot rebuild after bug.
- Recovery: restore source if possible.
- Prevention: raw immutable storage.

- Failure: No owner for gold metrics.
- Symptom: conflicting business numbers.
- Recovery: assign owner and certify metrics.
- Prevention: governance process.

## 12. Common Mistakes

- Mistake: Treating bronze as trusted data.
- Why it is wrong: bronze may contain duplicates and bad records.
- Better approach: expose silver/gold to most users.

- Mistake: Creating layers without meaning.
- Why it is wrong: bronze/silver/gold become folder names only.
- Better approach: define quality and consumer expectations per layer.

## 13. Mini Example

```text
bronze.orders_raw:
raw JSON orders

silver.orders_clean:
typed, deduped, valid orders

gold.daily_revenue:
revenue by date, region, product
```

## 14. Interview Questions

1. What is Medallion architecture?
2. Bronze vs silver vs gold?
3. Why keep raw bronze data?
4. Where do quality checks fit?
5. Who consumes gold data?

## 15. Interview Speak

"Medallion architecture organizes lakehouse data into bronze raw, silver cleaned, and gold business-ready layers. It improves trust and replayability by making data quality and business meaning increase layer by layer."

## 16. Quick Recall

- One-line summary: Medallion architecture turns raw data into trusted business data through layers.
- Three keywords: bronze, silver, gold.
- One trap: Querying bronze as trusted data.
- One memory trick: Raw ingredients, cleaned prep, served meal.
