# Topic 163: Presto/Trino

## 1. Goal

Understand Presto/Trino as distributed SQL query engines that can query many data sources.

## 2. Baby Intuition

Trino is like a SQL translator and coordinator.

It does not need to own all the data. It can ask different storage systems for data and combine results through one SQL engine.

## 3. What It Is

- Simple definition: Presto/Trino is a distributed SQL query engine.
- Technical definition: Trino, originally forked from PrestoSQL, is a distributed SQL engine that executes analytical queries across data lakes, warehouses, databases, and connectors without necessarily storing the data itself.
- Category: Federated/distributed SQL query engine.
- Related terms: coordinator, worker, connector, catalog, split, exchange, data lake query.

## 4. Why It Exists

Companies store data in many places:

- S3/ADLS/GCS files
- Hive/Iceberg/Delta tables
- relational databases
- warehouses
- object stores
- Kafka in some setups

Trino exists to provide one SQL engine across many sources.

## 5. Where It Fits In A Data Platform

```text
BI/analyst SQL
  -> Trino coordinator
  -> Trino workers
  -> connectors
  -> data lake / warehouse / databases
```

Trino is often used with data lakes and lakehouse table formats.

## 6. How It Works Step By Step

1. User submits SQL to coordinator.
2. Coordinator parses and plans the query.
3. Planner asks connectors for table metadata.
4. Query is split into tasks.
5. Workers read data through connectors.
6. Workers filter, project, join, aggregate, and exchange data.
7. Coordinator returns final result.

## 7. How To Use It Practically

Important concepts:

| Concept | Meaning |
|---|---|
| coordinator | accepts queries and plans work |
| worker | executes query tasks |
| connector | lets Trino read a data source |
| catalog | configured source namespace |
| split | chunk of work assigned to workers |

Example:

```sql
SELECT region, SUM(amount)
FROM lakehouse.sales.orders
WHERE order_date >= DATE '2026-07-01'
GROUP BY region;
```

## 8. Real-World Scenario

- Product/system: Unified analytics over lakehouse.
- Problem: Analysts need SQL on Iceberg tables in S3 and some reference data in PostgreSQL.
- How Trino helps: one query engine can use connectors to query different sources.
- What would go wrong without it: teams copy data around or use many separate query tools.

## 9. System Design Angle

Use Trino when:

- data is in a lake/lakehouse
- federated SQL is needed
- interactive queries matter
- separation of storage and query engine is desired
- many connectors are useful

Be careful with:

- large cross-source joins
- connector pushdown limitations
- memory-heavy joins
- cluster sizing
- security across catalogs

## 10. Trade-offs

| Pros | Cons |
|---|---|
| query many sources | does not magically make all sources fast |
| good lake SQL engine | operational cluster management |
| separates compute/storage | memory tuning matters |
| connector ecosystem | cross-source joins can be expensive |
| interactive analytics | not a storage format itself |

## 11. Failure Modes

- Failure: Huge join does not fit memory.
- Symptom: query fails or spills heavily.
- Recovery: rewrite query, partition, increase resources.
- Prevention: model data and use right join strategies.

- Failure: Connector cannot push filters.
- Symptom: too much data scanned remotely.
- Recovery: choose better connector/table format/query.
- Prevention: test predicate pushdown.

- Failure: Coordinator bottleneck.
- Symptom: query planning/coordination slow.
- Recovery: tune cluster and workload.
- Prevention: capacity planning and query limits.

## 12. Common Mistakes

- Mistake: Thinking Trino stores the data.
- Why it is wrong: it is mainly a query engine over external systems.
- Better approach: pair it with lakehouse/warehouse storage.

- Mistake: Joining huge tables across slow sources.
- Why it is wrong: data movement can dominate.
- Better approach: colocate/model large datasets in the lakehouse first.

## 13. Mini Example

```text
Trino query:
orders in Iceberg table
join small country reference table in PostgreSQL

Good when reference table is small.
Risky when both sides are huge and remote.
```

## 14. Interview Questions

1. What is Trino?
2. How is Trino different from Snowflake?
3. What are connectors?
4. What happens during a distributed query?
5. Why are cross-source joins risky?

## 15. Interview Speak

"Trino is a distributed SQL query engine, not primarily a storage system. It uses connectors to query data lakes, lakehouse tables, warehouses, and databases. I would use it for interactive/federated SQL, while being careful with predicate pushdown, large joins, memory, and source performance."

## 16. Quick Recall

- One-line summary: Trino runs SQL across many data sources.
- Three keywords: coordinator, worker, connector.
- One trap: Thinking Trino owns the data.
- One memory trick: SQL brain with many connectors.
