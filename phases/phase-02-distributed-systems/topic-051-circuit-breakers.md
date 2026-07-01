# Topic 051: Circuit Breakers

## Goal

Understand how circuit breakers prevent repeated calls to failing dependencies.

## Simple Explanation

A circuit breaker is like an electrical breaker.

If a dependency keeps failing, stop calling it for a while. This protects both your service and the failing dependency.

## Core Idea

- Definition: A circuit breaker blocks calls to an unhealthy dependency after failure thresholds are reached.
- Why it matters: It prevents cascading failures and retry storms.
- Related terms: closed, open, half-open, timeout, fallback, bulkhead.

## States

| State | Meaning |
|---|---|
| Closed | calls are allowed normally |
| Open | calls fail fast without reaching dependency |
| Half-open | a few test calls are allowed to check recovery |

## How It Works

1. Dependency starts failing.
2. Failure count or error rate crosses threshold.
3. Circuit opens.
4. Calls fail fast or use fallback.
5. After cooldown, circuit half-opens.
6. If test calls succeed, circuit closes.
7. If test calls fail, circuit opens again.

## Big Data / System Design Angle

Circuit breakers appear around:

- external APIs
- metadata stores
- feature services
- object storage calls
- downstream databases
- enrichment services in pipelines

Why they matter:

- prevent thread/connection exhaustion
- protect user-facing latency
- keep queues from exploding
- reduce load on failing dependencies

## Example

Fallback examples:

- return cached data
- skip optional enrichment
- write to queue for later processing
- degrade dashboard freshness
- show partial results

## Common Mistakes

- Mistake: No fallback plan.
- Better way: define what users or pipelines see while circuit is open.

- Mistake: Thresholds too sensitive.
- Better way: tune based on error rate, volume, and dependency behavior.

- Mistake: Circuit breaker without observability.
- Better way: alert on open circuits and dependency health.

## Interview Speak

"A circuit breaker protects a system from repeatedly calling a failing dependency. It moves between closed, open, and half-open states. I would use it with timeouts, retries, fallbacks, and alerts to prevent cascading failures."

## Quick Recall

- One-liner: Circuit breakers fail fast when dependencies are unhealthy.
- Keywords: open, half-open, fallback.
- Trap: Opening the circuit but having no fallback behavior.
