# Topic 001: What Is Data?

---

## 1. Intuition

Data is recorded information.

If life is happening, data is the notes we capture about it. A customer clicks a button, a bank card is swiped, a server returns an error, a patient gets a lab result, a driver changes location. Each event becomes data when we record it in a form a system can store, move, process, and query.

Beginner version:

- Data is a fact saved somewhere.
- Big Data is what happens when there are too many facts for one machine, one file, or one simple database process to handle comfortably.
- Data engineering is the discipline of collecting, cleaning, moving, storing, protecting, and serving those facts reliably.

Real-life analogy:

- A grocery bill is data about a shopping trip.
- A school attendance sheet is data about students.
- A GPS trail is data about movement over time.
- A log line is data about what software did at a specific moment.

---

## 2. Definition

- Definition: Data is a recorded representation of facts, events, measurements, observations, or states that can be stored, transmitted, processed, and analyzed.
- Category: Foundational concept in computer science, databases, analytics, machine learning, and distributed systems.
- Core idea: Convert real-world activity into machine-readable signals.
- Related concepts: information, records, events, files, tables, schemas, metadata, logs, metrics, features, transactions.

Important distinction:

- Data is raw recorded fact.
- Information is data interpreted in context.
- Knowledge is information used to make decisions.

Example:

```text
Data:        2026-07-01, user_42, item_99, click
Information: user_42 clicked item_99 on July 1, 2026
Knowledge:   user_42 may be interested in similar items
```

---

## 3. Why It Exists

Systems need memory.

Without data, software can only react in the moment. It cannot remember users, measure behavior, detect fraud, train models, debug incidents, recommend products, calculate revenue, or prove compliance.

Data exists because organizations need to answer questions like:

- What happened?
- When did it happen?
- Who did it affect?
- Why did it happen?
- What should we do next?
- Can we predict what will happen later?

Naive approaches fail when:

- data is too large for one machine
- data arrives continuously
- many teams need the same data
- data must be audited
- historical data must be replayed
- low-latency decisions are required
- data quality affects money, safety, or compliance

What breaks without treating data seriously:

- dashboards show wrong numbers
- ML models learn from bad inputs
- product decisions become guesses
- debugging production issues becomes slow
- compliance audits fail
- customers see stale or incorrect behavior

---

## 4. Where It Fits In Big Data

Data is the raw material of every layer.

| Layer | Role Of Data |
|---|---|
| Data source side | Applications, devices, databases, logs, sensors, and third-party APIs create data. |
| Ingestion layer | Data is collected through batch imports, message queues, event streams, CDC, or API pulls. |
| Storage layer | Data is saved in files, databases, warehouses, lakes, lakehouses, or object storage. |
| Processing layer | Data is cleaned, joined, aggregated, enriched, validated, or transformed. |
| Serving/query layer | Data is exposed to dashboards, APIs, ML models, reports, and business users. |
| Orchestration layer | Data workflows are scheduled, retried, monitored, and dependency-managed. |
| Monitoring/governance layer | Data quality, lineage, access, privacy, cost, and compliance are controlled. |
| System design relevance | Every architecture choice depends on data volume, velocity, variety, correctness, and access pattern. |

Simple Big Data flow:

```text
Sources
  -> Ingestion
  -> Raw Storage
  -> Processing
  -> Curated Storage
  -> Serving
  -> Users / Applications / ML
```

Example:

```text
Mobile app click
  -> Kafka
  -> S3 raw data lake
  -> Spark cleaning job
  -> Iceberg/Delta table
  -> Trino/BigQuery dashboard
  -> Product team decision
```

---

## 5. How It Works

At the most basic level, data moves through a lifecycle.

1. Input
   - Something happens in the real world or inside software.
   - Example: user clicks "Buy Now".

2. Capture
   - The system records the event.
   - Example event:

```json
{
  "event_id": "evt_1001",
  "user_id": "u42",
  "event_type": "button_click",
  "button": "buy_now",
  "created_at": "2026-07-01T10:15:30Z"
}
```

3. Validation
   - Check whether required fields exist and have expected types.
   - Example: `event_id`, `user_id`, and `created_at` must not be missing.

4. Movement
   - Send the data to another system.
   - Example: app server sends event to Kafka or Kinesis.

5. Storage
   - Save the data for later use.
   - Example: write raw JSON events into S3.

6. Processing
   - Clean, transform, join, aggregate, deduplicate, or enrich.
   - Example: convert raw clicks into daily user engagement metrics.

7. Serving
   - Make data available to users or systems.
   - Example: dashboard shows daily purchases.

8. Retention and deletion
   - Keep data for a legal, business, or technical period.
   - Delete or anonymize sensitive records when required.

Control flow:

- Orchestrators like Airflow decide when jobs run.
- Stream processors decide how events are consumed.
- Query engines decide how data is scanned and joined.

Data flow:

- Data moves from producers to storage and consumers.
- Movement can be batch, streaming, or request/response.

Metadata flow:

- Schemas describe fields.
- Catalogs describe where datasets live.
- Lineage describes where data came from and how it changed.

Important states:

- raw
- validated
- cleaned
- enriched
- aggregated
- served
- archived
- deleted

Failure path:

- Producer sends malformed data.
- Ingestion accepts or rejects it.
- Bad data may move to a dead letter queue.
- Monitoring alerts the owning team.

Recovery path:

- Fix producer or schema.
- Replay events from source or queue.
- Backfill corrected data.
- Recompute derived tables.

---

## 6. How To Use It

A data engineer uses data by first understanding its shape, meaning, and access pattern.

Practical workflow:

1. Identify the source.
2. Understand the fields.
3. Define the schema.
4. Decide whether the data is batch or streaming.
5. Choose a storage format.
6. Add validation.
7. Build transformation logic.
8. Expose the result to consumers.
9. Monitor freshness, quality, volume, and failures.

Example data record:

```json
{
  "order_id": "o1001",
  "customer_id": "c2001",
  "amount_usd": 49.99,
  "status": "paid",
  "created_at": "2026-07-01T12:30:00Z"
}
```

Example SQL usage:

```sql
SELECT
    DATE(created_at) AS order_date,
    COUNT(*) AS paid_orders,
    SUM(amount_usd) AS revenue_usd
FROM orders
WHERE status = 'paid'
GROUP BY DATE(created_at)
ORDER BY order_date;
```

Production usage pattern:

- Keep raw data immutable when possible.
- Validate data before trusting it.
- Use schemas for important datasets.
- Track lineage for derived data.
- Monitor freshness and correctness.
- Protect sensitive fields like PII and PHI.

---

## 7. What Problem It Solves

- Primary problem solved: Represents real-world activity in a form software can store, process, analyze, and use for decisions.
- Secondary benefits: Measurement, automation, personalization, auditing, debugging, forecasting, and compliance.
- Systems impact: Drives choices around storage, processing, schemas, partitioning, indexing, replication, retention, and security.
- Business impact: Enables analytics, reporting, product optimization, fraud detection, ML, experimentation, and operational visibility.
- Interview relevance: Every Big Data system design starts by clarifying the data: volume, shape, velocity, correctness, ownership, and consumers.

---

## 8. When To Use It

Use data intentionally whenever a system needs to:

- remember state
- measure behavior
- answer business questions
- automate decisions
- support dashboards
- train ML models
- debug incidents
- audit user or system activity
- synchronize systems
- detect anomalies

Strong-fit scenarios:

- high-volume events
- historical analysis
- compliance reporting
- recommendation systems
- fraud detection
- observability platforms
- experimentation and A/B testing

Interview keywords that should trigger data thinking:

- analytics
- reporting
- metrics
- events
- logs
- real-time dashboard
- personalization
- fraud
- recommendations
- audit
- data lake
- warehouse
- pipeline

---

## 9. When Not To Use It

The mature answer is not "collect everything forever."

Avoid unnecessary data collection when:

- there is no clear use case
- data is sensitive and risky to store
- storage cost exceeds value
- the organization cannot govern access
- data quality will be too poor to trust
- collecting it violates privacy expectations
- real-time collection is unnecessary and batch is enough

Overkill examples:

- Using Kafka for a small daily CSV file.
- Using a data lake for 100 rows of config.
- Saving every debug log forever.
- Keeping PII when aggregated anonymous data is enough.

Better alternatives:

- Use a simple relational table for small structured data.
- Use logs with short retention for temporary debugging.
- Use aggregated metrics instead of raw events when raw detail is unnecessary.
- Use sampling when full capture is too expensive.
- Use anonymization or tokenization for sensitive fields.

---

## 10. Real-World Scenarios

### Scenario 1: Netflix Viewing Events

- Product/system: Streaming analytics platform.
- Problem: Understand what users watch, pause, skip, search, and abandon.
- How this topic helps: Each user action becomes event data that feeds recommendations, quality monitoring, and content decisions.
- What would go wrong without it: Netflix could not personalize home pages, measure engagement, detect playback issues, or evaluate content performance.

### Scenario 2: Uber Driver Location

- Product/system: Real-time ride marketplace.
- Problem: Match riders with nearby drivers and estimate arrival times.
- How this topic helps: GPS pings become data points for location, speed, heading, and availability.
- What would go wrong without it: Matching would be inaccurate, ETAs would drift, and supply-demand balancing would suffer.

### Scenario 3: Amazon Clickstream

- Product/system: E-commerce behavioral analytics.
- Problem: Understand searches, clicks, carts, purchases, and drop-offs.
- How this topic helps: Clickstream data reveals customer intent and powers recommendations, ranking, ads, and experiments.
- What would go wrong without it: The business would lose personalization, funnel analysis, and experimentation feedback.

### Scenario 4: Healthcare Claims

- Product/system: Claims analytics and compliance platform.
- Problem: Process claims while protecting PHI.
- How this topic helps: Structured claims data enables payment analysis, fraud checks, reporting, and regulatory controls.
- What would go wrong without it: Incorrect payments, audit failures, privacy breaches, and poor operational visibility.

---

## 11. System Design Considerations

In interviews, the first data question is usually:

```text
What data are we producing, storing, processing, and serving?
```

Where it appears in architecture diagrams:

- event schemas
- database tables
- message topics
- object storage paths
- warehouse tables
- feature stores
- dashboards
- audit logs

Scalability impact:

- More data means more storage, partitions, compute, network, and metadata.
- Large data requires distributed storage and processing.

Availability impact:

- If data ingestion is unavailable, downstream analytics become stale.
- If serving stores are unavailable, users may not see dashboards or recommendations.

Consistency impact:

- Some systems need strict correctness, like payments.
- Some systems tolerate eventual consistency, like daily engagement dashboards.

Latency impact:

- Real-time fraud detection may need milliseconds to seconds.
- Daily finance reports may tolerate hours.

Cost impact:

- Raw data storage is cheap in object stores, but processing and repeated scans can be expensive.
- Poor partitioning and bad file formats increase query cost.

Operational complexity:

- More datasets require ownership, quality checks, lineage, access control, and documentation.

Interviewer follow-ups to expect:

- What is the data schema?
- What is the data volume per day?
- Is it batch or streaming?
- What are freshness requirements?
- How do you handle duplicate events?
- How do you handle late events?
- How do you protect PII?
- How long do you retain raw data?
- Who consumes this data?

---

## 12. Pros And Cons

| Pros | Cons |
|---|---|
| Enables measurement and decision-making | Can be expensive to store and process |
| Supports automation, analytics, and ML | Bad data creates bad decisions |
| Helps debug and audit systems | Sensitive data increases security and compliance risk |
| Creates historical memory | Requires governance, ownership, and quality controls |
| Powers personalization and optimization | Data pipelines add operational complexity |

---

## 13. Trade-offs And Common Mistakes

### Trade-offs

- More raw data gives more flexibility, but increases storage, privacy, and governance burden.
- More validation improves trust, but can add latency and reject useful-but-imperfect records.
- Real-time data improves freshness, but costs more and is harder to operate than batch.
- Strong schemas improve reliability, but require schema evolution planning.
- Aggregated data is cheaper to query, but loses detail needed for debugging or replay.

Impact summary:

| Dimension | Design Pressure |
|---|---|
| Latency | Real-time capture and serving reduce delay but add complexity. |
| Throughput | High event volume requires partitioning, buffering, and distributed processing. |
| Consistency | Critical domains need stronger guarantees and reconciliation. |
| Cost | Storage may be cheap, but compute, scans, and operations can dominate. |
| Complexity | More datasets require catalogs, ownership, validation, and monitoring. |

### Common Mistakes

- Mistake: Thinking all data is equally valuable.
- Why it is wrong: Some data has low business value but high storage, privacy, or operational cost.
- Better approach: Collect data with a clear use case, owner, retention policy, and quality expectation.
- Interview-safe explanation: "I would separate must-have business events from nice-to-have diagnostic events and set different retention policies."

- Mistake: Ignoring schema.
- Why it is wrong: Producers may change field names or types and silently break downstream jobs.
- Better approach: Use schemas, compatibility rules, versioning, and validation.
- Interview-safe explanation: "I would define an event contract and enforce schema compatibility before downstream systems consume the data."

- Mistake: Trusting raw data directly in dashboards.
- Why it is wrong: Raw data can contain duplicates, late events, missing fields, or corrupt records.
- Better approach: Use raw, cleaned, and curated layers.
- Interview-safe explanation: "I would keep raw immutable data for replay, but serve metrics from validated curated tables."

- Mistake: Keeping sensitive data forever.
- Why it is wrong: It increases breach impact and compliance risk.
- Better approach: Minimize, mask, tokenize, encrypt, and enforce retention.
- Interview-safe explanation: "I would avoid storing PII unless needed and apply retention, encryption, and access controls."

---

## 14. Key Numbers

These are rough reasoning numbers, not universal constants.

### Basic Units

| Unit | Size |
|---|---:|
| 1 byte | 8 bits |
| 1 KB | about 1 thousand bytes |
| 1 MB | about 1 million bytes |
| 1 GB | about 1 billion bytes |
| 1 TB | about 1 trillion bytes |
| 1 PB | about 1 thousand TB |

### Data Scale Intuition

| Scenario | Approximate Scale |
|---|---:|
| Small CSV | KB to MB |
| Application database table | MB to TB |
| Daily clickstream for a large product | GB to many TB per day |
| Logs for many services | GB to PB per day |
| Enterprise data lake | TB to PB+ |
| Large ML training corpus | TB to PB+ |

### Interview Numbers To Ask For

- Events per second: 1K, 10K, 100K, 1M+
- Average event size: 500 bytes to 5 KB for many JSON events
- Daily raw data: event_size * events_per_second * 86,400
- Retention: days for logs, months/years for analytics, regulated periods for compliance
- Freshness: seconds for real-time, minutes for near-real-time, hours/days for batch
- Replication: commonly 3 copies in many distributed storage systems
- Partitioning: usually based on time, tenant, user, region, or entity id

Example estimate:

```text
100,000 events/sec * 1 KB/event * 86,400 sec/day
= 8,640,000,000 KB/day
= about 8.6 TB/day before compression and replication
```

---

## 15. Failure Modes

### Missing Data

- What fails: Producer does not emit events or ingestion drops records.
- User observes: Dashboards show lower counts or gaps.
- Recovery: Replay from source if available, backfill from logs, or mark the period incomplete.
- Mitigation: Monitor volume, freshness, and producer health.

### Duplicate Data

- What fails: Producer retries, consumer reprocesses, or job reruns without idempotency.
- User observes: Counts and revenue may be inflated.
- Recovery: Deduplicate using event id, natural key, or deterministic merge.
- Mitigation: Idempotent writes and unique event identifiers.

### Corrupt Or Malformed Data

- What fails: Bad JSON, missing fields, wrong data types, invalid timestamps.
- User observes: Pipeline failures or incorrect aggregates.
- Recovery: Send bad records to quarantine or dead letter queue.
- Mitigation: Schema validation and producer contracts.

### Late Data

- What fails: Events arrive after expected processing window.
- User observes: Dashboard numbers change after initial publication.
- Recovery: Reprocess affected windows.
- Mitigation: Watermarks, allowed lateness, and clear metric definitions.

### Sensitive Data Leakage

- What fails: PII or PHI appears in logs, events, or shared datasets.
- User observes: Compliance incident or access violation.
- Recovery: Revoke access, delete/mask data, audit exposure, rotate credentials if needed.
- Mitigation: Data classification, masking, encryption, access control, and retention rules.

### Metadata Loss

- What fails: Schema, catalog, or lineage information is missing or wrong.
- User observes: Teams cannot understand or trust datasets.
- Recovery: Rebuild catalog from source definitions and pipeline code.
- Mitigation: Maintain schemas, ownership, documentation, and lineage.

---

## 16. Code Sample

This small Python example shows how raw records become useful data only after parsing and validation.

```python
from datetime import datetime


raw_event = {
    "event_id": "evt_1001",
    "user_id": "u42",
    "event_type": "purchase",
    "amount_usd": "49.99",
    "created_at": "2026-07-01T10:15:30Z",
}


def parse_purchase_event(event):
    required_fields = ["event_id", "user_id", "event_type", "amount_usd", "created_at"]

    for field in required_fields:
        if field not in event:
            raise ValueError(f"Missing required field: {field}")

    return {
        "event_id": event["event_id"],
        "user_id": event["user_id"],
        "event_type": event["event_type"],
        "amount_usd": float(event["amount_usd"]),
        "created_at": datetime.fromisoformat(event["created_at"].replace("Z", "+00:00")),
    }


parsed_event = parse_purchase_event(raw_event)
print(parsed_event)
```

What this demonstrates:

- raw input is not automatically trustworthy
- validation protects downstream systems
- parsing converts strings into useful types
- typed records are easier to process and query

---

## 17. Mini Program / Simulation

This runnable example simulates a tiny clickstream pipeline.

Runnable file:

```text
phases/phase-00-foundations/examples/topic_001_clickstream_simulation.py
```

It does four things:

1. Receives raw events.
2. Validates required fields.
3. Separates bad records.
4. Aggregates valid events by event type.

```python
from collections import Counter


raw_events = [
    {"event_id": "e1", "user_id": "u1", "event_type": "view"},
    {"event_id": "e2", "user_id": "u1", "event_type": "click"},
    {"event_id": "e3", "user_id": "u2", "event_type": "purchase"},
    {"event_id": "e4", "event_type": "click"},
    {"user_id": "u3", "event_type": "view"},
    {"event_id": "e6", "user_id": "u4", "event_type": "view"},
]


REQUIRED_FIELDS = {"event_id", "user_id", "event_type"}


def is_valid(event):
    return REQUIRED_FIELDS.issubset(event.keys())


def main():
    valid_events = []
    bad_events = []

    for event in raw_events:
        if is_valid(event):
            valid_events.append(event)
        else:
            bad_events.append(event)

    counts = Counter(event["event_type"] for event in valid_events)

    print("Valid events:", len(valid_events))
    print("Bad events:", len(bad_events))
    print("Event counts:", dict(counts))
    print("Bad records:", bad_events)


if __name__ == "__main__":
    main()
```

Expected output:

```text
Valid events: 4
Bad events: 2
Event counts: {'view': 2, 'click': 1, 'purchase': 1}
Bad records: [{'event_id': 'e4', 'event_type': 'click'}, {'user_id': 'u3', 'event_type': 'view'}]
```

Production mapping:

- `raw_events` could be Kafka messages.
- `bad_events` could go to a dead letter queue.
- `counts` could become dashboard metrics.
- validation rules could come from a schema registry.

---

## 18. Practical Interview Question

> You are designing a clickstream analytics platform for an e-commerce company. What data would you collect, how would you structure it, and what trade-offs would you consider?

---

## 19. Strong Interview Answer

I would collect user interaction events such as page views, searches, product clicks, add-to-cart events, purchases, and checkout failures. I would define a clear event schema with fields like `event_id`, `user_id`, `session_id`, `event_type`, `product_id`, `timestamp`, `device`, and `region`.

In the architecture, application servers or clients would produce events into a durable ingestion layer like Kafka or Kinesis. Raw events would be stored immutably in object storage for replay. A streaming or batch processing layer would validate, deduplicate, enrich, and aggregate the data. Curated outputs would be written to a warehouse or lakehouse for dashboards, experimentation, and recommendation features.

The key trade-offs are freshness, cost, correctness, and privacy. Real-time analytics gives faster insight but increases operational complexity. Raw event storage enables replay but increases storage and governance burden. I would protect sensitive data with minimization, encryption, masking, and access control.

For failure handling, I would use unique event ids for deduplication, schema validation for bad events, a dead letter queue for malformed records, monitoring for event volume and freshness, and backfills when pipelines fail. If full real-time processing is not required, I would start with batch processing and add streaming only for use cases like fraud detection or live dashboards.

---

## 20. Revision Notes

- One-line summary: Data is recorded fact that systems store, move, process, and use to make decisions.
- Three keywords: facts, schema, lifecycle.
- One interview trap: Jumping into tools like Spark or Kafka before clarifying the data shape, volume, and access pattern.
- One memory trick: Real world -> record -> store -> process -> serve -> decide.
- One production warning: Bad, duplicated, late, or sensitive data can break dashboards, ML, money flows, and compliance.
