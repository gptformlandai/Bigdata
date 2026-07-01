# Topic 012: APIs And REST

## Goal

Understand APIs and REST well enough to collect data from services, expose data products, and design clean service boundaries.

## Simple Explanation

An API is a contract for how one system talks to another.

REST is a common API style that uses HTTP methods and resource URLs.

Example:

```text
GET /orders/o1
```

Means: "Give me order o1."

## Core Idea

- Definition: An API is an interface that exposes operations or data to other software. REST is an HTTP-based architectural style centered on resources.
- Why it matters: Data pipelines often ingest from APIs and serve results through APIs.
- Related terms: endpoint, request, response, JSON, status code, pagination, rate limit.

## REST Basics

| Method | Meaning | Example |
|---|---|---|
| GET | read | `GET /orders/o1` |
| POST | create | `POST /orders` |
| PUT | replace | `PUT /orders/o1` |
| PATCH | partial update | `PATCH /orders/o1` |
| DELETE | delete | `DELETE /orders/o1` |

Common status codes:

| Code | Meaning |
|---:|---|
| 200 | OK |
| 201 | Created |
| 400 | Bad request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not found |
| 429 | Too many requests |
| 500 | Server error |
| 503 | Service unavailable |

## How It Is Used

Data engineers use APIs to:

- pull data from SaaS systems
- publish ML features or metrics
- trigger jobs
- expose data quality results
- send events to ingestion services
- integrate with internal platforms

Important API concerns:

- pagination
- authentication
- rate limits
- retries
- idempotency
- schema changes
- timestamps and time zones

## Big Data / System Design Angle

APIs are not ideal for bulk Big Data transfer unless designed for it.

For small or medium pulls, REST is fine. For massive datasets, prefer:

- object storage exports
- database replication
- CDC
- streaming
- batch files

REST API ingestion risks:

- rate limits
- partial page failures
- duplicate pulls
- changing response schemas
- inconsistent snapshots

## Example

Simple API response:

```json
{
  "order_id": "o1",
  "customer_id": "c1",
  "amount": 49.99,
  "status": "paid"
}
```

Paginated response:

```json
{
  "items": [
    {"order_id": "o1"},
    {"order_id": "o2"}
  ],
  "next_page_token": "abc123"
}
```

## Common Mistakes

- Mistake: Forgetting pagination.
- Better way: Keep fetching until no next token exists.

- Mistake: Ignoring rate limits.
- Better way: Respect `429` responses and retry after delay.

- Mistake: Using REST for high-volume event streaming.
- Better way: Use Kafka, Kinesis, Pub/Sub, or files for high-throughput data movement.

## Interview Speak

"APIs are contracts between systems. REST APIs are useful for resource-oriented request/response access, but for Big Data ingestion I would check volume, rate limits, pagination, consistency, retries, and idempotency. For very large or continuous data, streaming or object storage export may be better."

## Quick Recall

- One-liner: APIs are software contracts; REST exposes resources over HTTP.
- Keywords: endpoint, status code, pagination.
- Trap: Pulling huge datasets through a rate-limited API when bulk export or CDC is better.
