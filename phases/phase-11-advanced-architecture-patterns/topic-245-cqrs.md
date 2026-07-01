# Topic 245: CQRS

## 1. Goal

Understand CQRS as separating write models from read models.

## 2. Baby Intuition

CQRS says:

```text
The way we update data does not have to be the same way we read data.
```

One model can be optimized for correctness of writes, another for fast queries.

## 3. What It Is

- Simple definition: CQRS separates commands/writes from queries/reads.
- Technical definition: Command Query Responsibility Segregation separates the model that handles state-changing commands from one or more read models optimized for queries.
- Category: Application and data serving pattern.
- Related terms: command, query, read model, write model, projection, event sourcing, eventual consistency.

## 4. Why It Exists

Write needs and read needs often conflict.

Writes need:

- validation
- transactions
- business rules
- consistency

Reads need:

- fast lookup
- denormalized views
- aggregations
- search
- dashboards

CQRS lets each side be optimized differently.

## 5. Where It Fits In A Data Platform

```text
write model / OLTP service
  -> events/CDC
  -> read models/search/warehouse/cache
```

Data platforms often build read models from operational writes.

## 6. How It Works Step By Step

1. Command updates write model.
2. Write model emits event or CDC change.
3. Projection pipeline consumes change.
4. Read model is updated.
5. Query reads from read model.
6. Read model may be eventually consistent with write model.

## 7. How To Use It Practically

Read model examples:

| Read Need | Read Model |
|---|---|
| product search | Elasticsearch/OpenSearch index |
| dashboard | warehouse aggregate table |
| user profile API | denormalized cache/table |
| recommendation | feature store/vector index |

Good practices:

- define freshness expectations
- monitor projection lag
- make projection idempotent
- handle deletes and schema changes
- expose consistency expectations to users

## 8. Real-World Scenario

- Product/system: E-commerce product catalog.
- Problem: Product service owns writes, but users need fast search by text/category/price.
- How CQRS helps: product DB is write model; search index is read model built from events/CDC.
- What would go wrong without it: transactional database gets overloaded by search queries.

## 9. System Design Angle

Use CQRS when:

- read and write workloads differ greatly
- query performance needs denormalized/indexed views
- event-driven projections are acceptable
- eventual consistency is acceptable

Avoid when:

- simple CRUD app is enough
- users require immediate read-after-write everywhere
- projection complexity is not justified

## 10. Trade-offs

| Pros | Cons |
|---|---|
| optimized read models | eventual consistency |
| protects write DB | more moving parts |
| supports search/analytics | projection lag |
| multiple read views | duplicate data |

## 11. Failure Modes

- Failure: Projection consumer down.
- Symptom: read model stale.
- Recovery: restart/replay.
- Prevention: lag alerts.

- Failure: Delete not propagated.
- Symptom: removed item still searchable.
- Recovery: repair/replay.
- Prevention: delete handling tests.

- Failure: User expects instant consistency.
- Symptom: confusion after write.
- Recovery: UX/status messaging or read own write path.
- Prevention: define consistency contract.

## 12. Common Mistakes

- Mistake: Using CQRS for every service.
- Why it is wrong: it adds complexity.
- Better approach: use it where read/write needs strongly differ.

- Mistake: No reconciliation between models.
- Why it is wrong: read model can drift forever.
- Better approach: monitoring and periodic consistency checks.

## 13. Mini Example

```text
Write:
Product service updates product price in OLTP DB

Event:
ProductPriceChanged

Read:
Search index updates price for product results
```

## 14. Interview Questions

1. What is CQRS?
2. Why separate read and write models?
3. How does CQRS relate to event sourcing?
4. What is projection lag?
5. When is CQRS overkill?

## 15. Interview Speak

"CQRS separates the write model from read models. Writes stay correct and transactional, while read models can be denormalized for search, dashboards, APIs, or analytics. The trade-off is duplicate data and eventual consistency, so projection lag and reconciliation matter."

## 16. Quick Recall

- One-line summary: CQRS separates writes from optimized reads.
- Three keywords: command, query, projection.
- One trap: Using it when CRUD is enough.
- One memory trick: One desk for updates, another for reading.
