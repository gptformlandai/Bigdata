# Topic 014: Indexes

## Goal

Understand how indexes speed up reads, why they slow down writes, and when they matter in system design.

## Simple Explanation

An index is like the index at the back of a book.

Without an index, the database may scan every page. With an index, it can jump closer to the rows it needs.

## Core Idea

- Definition: An index is an auxiliary data structure that helps a database find rows faster.
- Why it matters: Indexes reduce read latency for selective lookups and filters.
- Related terms: B-tree, hash index, primary key, secondary index, selectivity, covering index.

## How It Works

Without index:

```text
scan every row -> check condition -> return matches
```

With index:

```text
search index -> locate matching row ids -> fetch rows
```

Common index types:

| Type | Best For |
|---|---|
| B-tree | equality and range queries |
| Hash index | equality lookups |
| Composite index | multi-column filters |
| Full-text index | text search |
| Bitmap index | low-cardinality analytical filters |

## Example

Query:

```sql
SELECT *
FROM orders
WHERE customer_id = 'c1';
```

Index:

```sql
CREATE INDEX idx_orders_customer_id
ON orders(customer_id);
```

This helps if `customer_id = 'c1'` matches a small portion of the table.

## Trade-offs

| Benefit | Cost |
|---|---|
| Faster reads | Slower writes |
| Faster filters and joins | More storage |
| Can enforce uniqueness | Index maintenance overhead |
| Can avoid full table scans | Too many indexes confuse planning and operations |

## Big Data / System Design Angle

Indexes are central in OLTP databases, but Big Data systems often use related ideas:

- partition pruning
- clustering
- sorting
- min/max statistics
- bloom filters
- data skipping
- materialized views

In warehouses and lakehouses, you may not create traditional B-tree indexes on every table. Instead, you optimize layout so query engines scan less data.

Interview trigger words:

- low-latency lookup
- query is slow
- filter by user id
- range query
- database read performance
- high write rate

## Common Mistakes

- Mistake: Indexing every column.
- Better way: Index columns used frequently in selective filters, joins, and ordering.

- Mistake: Ignoring write overhead.
- Better way: Remember every insert/update/delete may update indexes.

- Mistake: Assuming indexes help low-selectivity queries.
- Better way: If a query returns most rows, a scan may be cheaper.

- Mistake: Using the wrong composite index order.
- Better way: Match index order to common query predicates.

## Failure / Stress Modes

- Too many indexes slow ingestion.
- Missing indexes cause high CPU and full scans.
- Skewed values reduce index usefulness.
- Large indexes may not fit in memory.
- Stale statistics can lead to bad query plans.

## Interview Speak

"Indexes speed up reads by maintaining a lookup structure, usually a B-tree for range and equality queries. The trade-off is extra storage and slower writes because the index must be updated. I would add indexes based on query patterns and selectivity, not blindly on every column."

## Quick Recall

- One-liner: Indexes trade write cost and storage for faster reads.
- Keywords: B-tree, selectivity, write overhead.
- Trap: Thinking indexes always make queries faster.
