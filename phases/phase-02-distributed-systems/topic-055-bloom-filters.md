# Topic 055: Bloom Filters

## Goal

Understand Bloom filters as memory-efficient structures for checking whether something is definitely absent or maybe present.

## Simple Explanation

A Bloom filter answers:

```text
Have I possibly seen this item before?
```

It can say:

- definitely no
- maybe yes

It cannot say:

- definitely yes

## Core Idea

- Definition: A Bloom filter is a probabilistic data structure for set membership tests.
- Why it matters: It saves memory and avoids expensive lookups.
- Related terms: false positive, hash function, bit array, membership test.

## How It Works

1. Start with a bit array of zeros.
2. Use multiple hash functions.
3. To add an item, hash it and set several bit positions to 1.
4. To check an item, hash it and inspect those positions.
5. If any position is 0, item is definitely absent.
6. If all positions are 1, item may be present.

## False Positives

Bloom filters can return false positives:

```text
filter says maybe present, but item was never inserted
```

They do not return false negatives if implemented correctly:

```text
if filter says absent, item is absent
```

## Big Data / System Design Angle

Used in:

- databases before disk lookup
- LSM-tree storage engines
- distributed caches
- web crawlers
- deduplication pre-checks
- stream processing
- Parquet/ORC-like filtering concepts

Example:

Before checking a slow database, use Bloom filter:

```text
if definitely absent -> skip expensive lookup
if maybe present -> query database
```

## Trade-offs

| Gain | Cost |
|---|---|
| very memory efficient | false positives |
| fast lookups | cannot list items |
| avoids expensive reads | deletion is hard in standard Bloom filters |
| scalable pre-filter | needs tuning |

## Common Mistakes

- Mistake: Treating "maybe present" as definitely present.
- Better way: verify with real storage.

- Mistake: Using Bloom filters when false positives are unacceptable.
- Better way: use exact set/index.

- Mistake: Forgetting sizing.
- Better way: choose bit array size and hash count based on expected items and false-positive rate.

## Interview Speak

"A Bloom filter is a probabilistic membership structure. It can say definitely not present or maybe present. It is useful to avoid expensive disk or network lookups, but false positives are possible, so a maybe result must be verified."

## Quick Recall

- One-liner: Bloom filter says definitely no or maybe yes.
- Keywords: probabilistic, false positive, bit array.
- Trap: Treating maybe as truth.
