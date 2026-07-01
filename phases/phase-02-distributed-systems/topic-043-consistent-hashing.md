# Topic 043: Consistent Hashing

## Goal

Understand how consistent hashing reduces data movement when nodes are added or removed.

## Simple Explanation

Normal hashing can reshuffle almost everything when the number of servers changes.

Consistent hashing puts servers and keys on a ring so adding or removing a server only moves nearby keys.

## Core Idea

- Definition: Consistent hashing maps keys and nodes onto a hash ring so membership changes move only a fraction of keys.
- Why it matters: Distributed caches, databases, and storage systems need to rebalance without moving all data.
- Related terms: hash ring, virtual nodes, rebalancing, cache cluster, partitioning.

## Why Normal Hashing Hurts

Simple modulo hashing:

```text
hash(key) % number_of_nodes
```

If `number_of_nodes` changes from 4 to 5, most keys may map to different nodes.

That means:

- cache misses spike
- data migration becomes huge
- cluster changes are expensive

## How Consistent Hashing Works

1. Hash each node onto a ring.
2. Hash each key onto the same ring.
3. Store the key on the first node clockwise from the key position.
4. When a node joins, it takes only part of a neighbor's range.
5. When a node leaves, its range moves to the next node.

Virtual nodes improve balance:

```text
one physical node -> many positions on the ring
```

## Big Data / System Design Angle

Used in:

- distributed caches
- key-value stores
- Cassandra-style systems
- Dynamo-style systems
- load distribution
- storage rings

Benefits:

- less reshuffling
- smoother scaling
- better fault tolerance

Costs:

- implementation complexity
- uneven distribution without virtual nodes
- range movement still required

## Example

```text
Ring:
0 ---- A ---- key1 ---- B ---- key2 ---- C ---- 100

key1 goes to B
key2 goes to C
```

If node B disappears, key1 moves to C, but not every key in the system moves.

## Common Mistakes

- Mistake: Using modulo hashing for dynamic clusters.
- Better way: Use consistent hashing or a managed partition map.

- Mistake: Forgetting virtual nodes.
- Better way: Use virtual nodes to smooth load distribution.

- Mistake: Thinking no data moves.
- Better way: Only less data moves, not zero data.

## Interview Speak

"Consistent hashing maps keys and nodes onto a ring so adding or removing nodes moves only a limited range of keys. It is useful for distributed caches and key-value stores because it avoids massive reshuffling compared to `hash(key) % node_count`. Virtual nodes help balance load."

## Quick Recall

- One-liner: Consistent hashing keeps cluster changes from moving everything.
- Keywords: ring, virtual nodes, rebalancing.
- Trap: Forgetting that some movement still happens.
