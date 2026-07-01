# Topic 263: Design Log Aggregation System

## 1. Goal

Design a centralized logging platform that collects, stores, searches, and retains logs from many services.

## 2. Baby Intuition

Every service writes a diary.

A log aggregation system collects all diaries into one searchable place so engineers can debug incidents.

## 3. Requirements

Clarify:

- Are logs for debugging, security audit, compliance, or all?
- What query latency is expected?
- How long should logs be retained?
- What log volume is expected?
- Do we need full-text search or label-based search?

## 4. Functional Requirements

- collect logs from apps, containers, hosts, and jobs
- parse and enrich logs with metadata
- store logs for search and retention
- support querying by service, time, level, trace_id, request_id
- alert on error patterns
- protect sensitive data
- support hot and cold storage tiers

## 5. Non-Functional Requirements

- high ingestion throughput
- backpressure and buffering
- durable storage
- fast enough search for recent logs
- cost-efficient retention
- access control by team/service
- redaction for secrets and sensitive data

## 6. Capacity Estimation

Example:

```text
10K services/containers
1 KB average log line
100K log lines/sec peak
= about 100 MB/sec raw
= about 8.6 TB/day before compression
```

Log volume can explode during incidents, so buffering and sampling matter.

## 7. Events And APIs

Structured log:

```json
{
  "timestamp": "2026-07-02T10:00:00Z",
  "level": "ERROR",
  "service": "checkout-api",
  "env": "prod",
  "trace_id": "tr1",
  "message": "payment timeout",
  "status_code": 504
}
```

Query:

```text
service="checkout-api" level="ERROR" trace_id="tr1" time=last_30m
```

## 8. Data Model

Hot index:

```text
logs_hot(timestamp, service, env, level, trace_id, message, parsed_fields)
```

Cold archive:

```text
logs_archive/date=YYYY-MM-DD/service=checkout-api/files
```

## 9. High-Level Architecture

```text
apps/containers/hosts
  -> log agent
  -> local buffer
  -> Kafka or log ingestion service
  -> parser/enricher/redactor
  -> hot search index
  -> cold object storage archive
```

## 10. Data Flow

1. App writes structured logs to stdout/file.
2. Agent reads logs and adds metadata.
3. Agent buffers locally during network issues.
4. Logs are sent to broker or ingestion service.
5. Parser extracts fields and redacts secrets.
6. Recent logs are indexed for search.
7. Older logs are archived to object storage.
8. Retention policy deletes expired logs.

## 11. Deep Dive Components

Indexing strategy:

- index timestamp, service, env, level, trace_id
- avoid indexing every random field
- route logs by tenant/team if needed

Retention tiers:

- hot searchable logs: days to weeks
- warm/cold logs: weeks to months
- compliance archive: policy-driven

Sensitive data:

- redact tokens/passwords
- block known secret patterns
- restrict logs containing PII/PHI

## 12. Scaling And Partitioning

- Partition broker by service or tenant.
- Partition storage by date and service.
- Scale indexers independently from collectors.
- Use rate limits/sampling for noisy services.
- Use multi-tenant quotas to prevent one service from overwhelming the platform.

## 13. Consistency And Correctness

- Logging usually prefers availability over perfect consistency.
- Some log loss may be acceptable for debug logs, not for audit logs.
- Audit/security logs may need stronger durability and immutability.
- Use at-least-once delivery and tolerate duplicates in search.

## 14. Failure Handling

| Failure | Handling |
|---|---|
| ingestion down | local agent buffering |
| broker lag | scale consumers/indexers |
| index down | continue archive writes |
| log storm | rate limit or sample noisy source |
| sensitive data leak | purge/redact and rotate secrets |

## 15. Monitoring, Cost, And Security

Monitor:

- ingest rate
- dropped logs
- agent buffer size
- broker lag
- index latency
- query latency
- storage growth

Cost:

- control retention
- separate hot and cold storage
- avoid over-indexing
- sample debug logs

Security:

- redact secrets
- encrypt storage
- restrict team/service access
- audit searches for sensitive logs

## 16. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| full-text indexing | flexible search | expensive |
| label-based logs | cheaper | less flexible search |
| long retention | better investigations | high storage cost |
| sampling | cost control | may miss rare events |

## 17. Interview-Ready Final Answer

"I would build logging as an agent-based collection system. Applications write structured logs, agents enrich and buffer them, and logs flow through Kafka or an ingestion service into parsing/redaction. Recent logs go into a hot search index for debugging, while all or selected logs are archived to object storage with retention policies. I would monitor ingestion lag, dropped logs, query latency, and storage growth. The key concerns are log storms, indexing cost, sensitive data redaction, team-level access control, and separating best-effort debug logs from durable audit logs."

## 18. Quick Recall

- One-line summary: Log aggregation collects service diaries into searchable storage.
- Core tools: agents, buffer, Kafka, parser, search index, object archive.
- Main trap: indexing everything forever.
- Memory trick: searchable service diary.

