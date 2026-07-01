# Topic 174: Slowly Changing Dimensions

## 1. Goal

Understand how warehouses handle dimension attributes that change over time.

## 2. Baby Intuition

A customer can move from Texas to California.

For old reports, should last year's order count under Texas or California? Slowly changing dimensions answer this kind of question.

## 3. What It Is

- Simple definition: Slowly changing dimensions track changes in descriptive attributes over time.
- Technical definition: SCD patterns define how dimension tables preserve, overwrite, or version changes to attributes so historical facts can be reported correctly.
- Category: Dimensional modeling and history management.
- Related terms: SCD Type 1, Type 2, Type 3, effective date, current flag, surrogate key.

## 4. Why It Exists

Dimension values change:

- customer address
- product category
- employee department
- account tier
- store region

Analytics must decide whether history should:

- show the old value
- show the latest value
- show both current and previous value

## 5. Where It Fits In A Data Platform

```text
source dimension changes
  -> dimension table SCD logic
  -> facts join to correct dimension version
  -> historical reports stay meaningful
```

## 6. How It Works Step By Step

Common SCD types:

| Type | Behavior | Example |
|---|---|---|
| Type 1 | overwrite old value | fix typo in name |
| Type 2 | create new version row | customer changes segment |
| Type 3 | store limited previous value | previous_region column |

SCD Type 2 flow:

1. Existing dimension row is current.
2. New source record arrives with changed attribute.
3. Old row is closed with an end date/current flag false.
4. New row is inserted with new surrogate key.
5. Facts join based on event date or assigned dimension key.

## 7. How To Use It Practically

Type 2 columns:

```text
customer_key
customer_id
segment
effective_start_date
effective_end_date
is_current
```

Example:

```text
customer_id=10, segment=free, start=2026-01-01, end=2026-06-30
customer_id=10, segment=premium, start=2026-07-01, end=null, current=true
```

## 8. Real-World Scenario

- Product/system: Subscription analytics.
- Problem: Customer upgrades from free to premium in July.
- How SCD helps: January revenue can report under free segment, August revenue under premium segment.
- What would go wrong without it: historical reports may rewrite the past with today's customer segment.

## 9. System Design Angle

Ask:

- Does history matter for this attribute?
- Should reports use current value or historical value?
- What is the natural/business key?
- What is the surrogate key?
- How are late-arriving facts handled?
- What is the effective date?

Rule:

```text
Use Type 1 for corrections.
Use Type 2 when historical truth matters.
```

## 10. Trade-offs

| Approach | Pros | Cons |
|---|---|---|
| Type 1 | simple, latest value | loses history |
| Type 2 | preserves history | more rows and join complexity |
| Type 3 | simple limited history | only tracks small number of changes |

## 11. Failure Modes

- Failure: Type 1 used when history matters.
- Symptom: past reports change unexpectedly.
- Recovery: rebuild from history if available.
- Prevention: classify dimension attributes.

- Failure: Overlapping Type 2 date ranges.
- Symptom: facts join to multiple dimension rows.
- Recovery: fix ranges and constraints.
- Prevention: SCD validation tests.

- Failure: Late-arriving fact.
- Symptom: joins to wrong dimension version.
- Recovery: reprocess with event date logic.
- Prevention: handle event-time joins.

## 12. Common Mistakes

- Mistake: Using current dimension row for all historical facts.
- Why it is wrong: it rewrites history.
- Better approach: use Type 2 for attributes where history matters.

- Mistake: No current flag or date range.
- Why it is wrong: latest row and historical row are hard to identify.
- Better approach: include effective dates and current indicator.

## 13. Mini Example

```text
Order on 2026-06-15 -> customer segment free
Order on 2026-07-15 -> customer segment premium

Type 2 dimension preserves both truths.
```

## 14. Interview Questions

1. What is an SCD?
2. Type 1 vs Type 2?
3. When use Type 2?
4. What are effective dates?
5. How do late-arriving facts affect SCD joins?

## 15. Interview Speak

"Slowly changing dimensions handle changes to descriptive attributes. Type 1 overwrites and is useful for corrections. Type 2 creates a new version row with effective dates and current flag, preserving historical reporting. The key design decision is whether business reports need current truth or historical truth."

## 16. Quick Recall

- One-line summary: SCDs decide how dimension changes affect history.
- Three keywords: Type 1, Type 2, effective dates.
- One trap: Rewriting history accidentally.
- One memory trick: Did the past move with the customer?
