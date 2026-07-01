# Topic 170: OLAP Cubes

## 1. Goal

Understand OLAP cubes as pre-aggregated multi-dimensional analytics structures.

## 2. Baby Intuition

An OLAP cube is like a business scoreboard with many knobs.

You can slice revenue by date, region, product, channel, or combinations without recalculating everything from raw events.

## 3. What It Is

- Simple definition: An OLAP cube precomputes metrics across dimensions.
- Technical definition: An OLAP cube is a multidimensional analytical structure that stores measures aggregated by combinations of dimensions to support fast slice, dice, drill-down, and roll-up queries.
- Category: Analytical precomputation/modeling.
- Related terms: measure, dimension, hierarchy, rollup, drill-down, slice, dice, aggregate.

## 4. Why It Exists

Business users ask repeated questions:

- revenue by month
- revenue by region
- revenue by product
- revenue by month and region
- revenue by product category and channel

Cubes precompute or organize these combinations for fast exploration.

## 5. Where It Fits In A Data Platform

```text
warehouse fact/dimension tables
  -> cube/semantic layer/precomputed aggregates
  -> BI dashboards and business users
```

Modern systems may implement cube ideas through semantic layers, aggregate tables, materialized views, or OLAP engines.

## 6. How It Works Step By Step

1. Choose measures, such as revenue or count.
2. Choose dimensions, such as date, region, product.
3. Define hierarchies, such as day -> month -> quarter -> year.
4. Precompute aggregates for useful combinations.
5. BI users slice/dice data.
6. Queries read aggregates instead of raw transactions when possible.

## 7. How To Use It Practically

Core terms:

| Term | Meaning |
|---|---|
| measure | numeric metric like revenue |
| dimension | descriptive axis like region |
| hierarchy | levels like day/month/year |
| slice | filter one dimension |
| dice | filter multiple dimensions |
| roll-up | aggregate to higher level |
| drill-down | go to more detail |

## 8. Real-World Scenario

- Product/system: Sales analytics.
- Problem: Sales leaders explore revenue by time, region, product, and channel.
- How cube helps: common metric combinations are pre-aggregated for fast BI.
- What would go wrong without it: every interaction scans and groups raw sales rows.

## 9. System Design Angle

Use cube-like design when:

- business metrics are repeated
- dimensions are well-known
- dashboard interactivity matters
- raw detail is large
- consistency of metrics matters

Be careful with:

- too many dimensions
- high cardinality
- freshness
- storage explosion
- metric governance

## 10. Trade-offs

| Pros | Cons |
|---|---|
| very fast repeated analytics | storage/precompute cost |
| business-friendly dimensions | cube explosion risk |
| consistent metric definitions | refresh complexity |
| supports drill-down/roll-up | less flexible than raw SQL |

## 11. Failure Modes

- Failure: Too many dimension combinations.
- Symptom: cube becomes huge.
- Recovery: reduce dimensions/precompute only common paths.
- Prevention: model from real usage.

- Failure: Stale cube.
- Symptom: dashboard lags source data.
- Recovery: refresh/rebuild.
- Prevention: freshness monitoring.

- Failure: Wrong metric definition.
- Symptom: business loses trust.
- Recovery: correct metric and backfill.
- Prevention: metric governance.

## 12. Common Mistakes

- Mistake: Precomputing every possible combination.
- Why it is wrong: dimensions multiply quickly.
- Better approach: precompute high-value aggregates.

- Mistake: Ignoring raw drill-through needs.
- Why it is wrong: users may need transaction detail.
- Better approach: keep facts available for deeper investigation.

## 13. Mini Example

```text
Measure:
revenue

Dimensions:
date, region, product

Possible view:
revenue by month by region by product_category
```

## 14. Interview Questions

1. What is an OLAP cube?
2. Measures vs dimensions?
3. What are slice, dice, roll-up, drill-down?
4. Why can cubes explode in size?
5. Cubes vs materialized views?

## 15. Interview Speak

"An OLAP cube organizes or precomputes measures across dimensions so BI users can slice, dice, roll up, and drill down quickly. It improves dashboard performance and metric consistency, but too many dimensions can create storage and refresh complexity."

## 16. Quick Recall

- One-line summary: OLAP cubes precompute metrics across business dimensions.
- Three keywords: measures, dimensions, rollup.
- One trap: Cube explosion from too many dimensions.
- One memory trick: Business scoreboard with knobs.
