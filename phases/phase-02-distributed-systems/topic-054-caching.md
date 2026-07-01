# Topic 054: Caching

## Goal

Understand caching as a performance technique and know the correctness trade-offs it creates.

## Simple Explanation

A cache stores frequently used data closer to where it is needed.

Instead of recomputing or refetching the same value again and again, the system reuses a saved copy.

## Core Idea

- Definition: A cache is a fast temporary storage layer for frequently accessed or expensive-to-compute data.
- Why it matters: Caching reduces latency, database load, and compute cost.
- Related terms: TTL, cache hit, cache miss, eviction, invalidation, Redis, CDN.

## Common Cache Types

| Type | Example | Use |
|---|---|---|
| In-memory local cache | application memory | fastest, per-instance |
| Distributed cache | Redis, Memcached | shared across services |
| CDN | CloudFront, Akamai | static/global content |
| Query result cache | warehouse/query engine | repeated analytics queries |
| Metadata cache | schema/catalog lookup | reduce control-plane calls |

## Cache Patterns

Cache-aside:

1. App checks cache.
2. If hit, return.
3. If miss, read database.
4. Store result in cache.
5. Return result.

Write-through:

- write cache and database together

Write-behind:

- write cache first, database later

TTL:

- cached value expires after a configured time

## Big Data / System Design Angle

Caching helps:

- reduce p95/p99 latency
- protect databases
- reduce repeated warehouse scans
- speed up feature lookups
- serve dashboards faster

But caching introduces:

- stale data
- invalidation complexity
- hot keys
- memory cost
- cache stampedes

## Common Problems

Cache stampede:

```text
popular key expires -> many requests hit database at once
```

Mitigations:

- jittered TTL
- request coalescing
- early refresh
- rate limiting
- fallback stale cache

Hot key:

```text
one key receives huge traffic
```

Mitigations:

- replicate hot values
- local cache
- key splitting
- CDN

## Common Mistakes

- Mistake: Caching without deciding stale tolerance.
- Better way: define TTL and freshness requirement.

- Mistake: Forgetting invalidation.
- Better way: choose TTL, event-based invalidation, or write-through carefully.

- Mistake: Using cache as source of truth.
- Better way: cache should usually be rebuildable from durable storage.

## Interview Speak

"Caching reduces latency and backend load by storing frequently accessed data in a faster layer. I would define TTL, invalidation strategy, stale-data tolerance, and stampede protection. For correctness-critical data, I would be careful about serving stale values."

## Quick Recall

- One-liner: Cache saves time by reusing nearby data.
- Keywords: TTL, hit, invalidation.
- Trap: Treating cache as always fresh.
