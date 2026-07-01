# Topic 262: Design Real-Time Ad Analytics

## 1. Goal

Design a system that tracks ad impressions, clicks, conversions, spend, pacing, and campaign performance in near real time.

## 2. Baby Intuition

Ad analytics is a scoreboard for advertisers.

Advertisers want to know:

```text
how many people saw the ad,
how many clicked,
how much money was spent,
and whether conversions happened
```

## 3. Requirements

Clarify:

- Are we designing advertiser dashboards, billing, pacing, or attribution?
- What freshness is required?
- Are numbers approximate or billing-grade?
- How are conversions attributed?
- Do we need fraud/bot detection?

## 4. Functional Requirements

- collect ad impression, click, conversion, bid, and spend events
- compute campaign/ad/creative metrics
- support real-time spend pacing
- support advertiser dashboards
- support attribution windows
- detect invalid traffic
- generate billing-grade reconciled reports

## 5. Non-Functional Requirements

- high throughput and burst handling
- low-latency campaign metrics
- stronger correctness for billing/spend
- dedupe for clicks/conversions
- late conversion handling
- privacy and consent compliance
- high availability

## 6. Capacity Estimation

Example:

```text
50B ad impressions/day
1B clicks/day
100M conversions/day

impression events are largest volume
click/conversion events need stronger correctness
```

Ad systems often tolerate approximate live dashboards but require reconciled billing.

## 7. Events And APIs

Impression event:

```json
{
  "impression_id": "imp1",
  "campaign_id": "c1",
  "ad_id": "a1",
  "advertiser_id": "adv1",
  "cost_micros": 1200,
  "user_id_hash": "u1",
  "placement": "feed",
  "event_time": "2026-07-02T10:00:00Z"
}
```

Click event:

```json
{
  "click_id": "clk1",
  "impression_id": "imp1",
  "campaign_id": "c1",
  "event_time": "2026-07-02T10:01:00Z"
}
```

## 8. Data Model

Fact tables:

```text
ad_impressions(event_date, impression_id, campaign_id, ad_id, advertiser_id, cost_micros, placement)
ad_clicks(event_date, click_id, impression_id, campaign_id)
ad_conversions(event_date, conversion_id, click_id, campaign_id, revenue_micros)
```

Aggregate:

```text
campaign_minute_metrics(window_start, campaign_id, impressions, clicks, spend_micros, conversions)
```

## 9. High-Level Architecture

```text
ad serving system
  -> impression/click/conversion events
  -> Kafka/Pub/Sub
  -> stream aggregation
  -> real-time OLAP/dashboard and pacing service

Kafka/Pub/Sub
  -> lakehouse
  -> batch reconciliation
  -> warehouse billing reports
```

## 10. Data Flow

1. Ad server emits impression and spend events.
2. Click tracker emits click events.
3. Conversion tracker emits conversion events, often delayed.
4. Stream job dedupes and aggregates metrics by campaign/time.
5. Pacing service reads near-real-time spend.
6. Raw events land in lakehouse.
7. Batch jobs reconcile billing and attribution.
8. Advertiser dashboard reads real-time and finalized metrics.

## 11. Deep Dive Components

Attribution:

- connect conversion back to click or impression
- use attribution window such as 1 day click or 7 day view
- late conversions update old campaign metrics

Pacing:

- compare actual spend vs budget schedule
- slow down or speed up serving
- needs fresh spend metrics

Invalid traffic:

- bot clicks
- duplicate clicks
- suspicious conversion bursts
- internal/test traffic

## 12. Scaling And Partitioning

- Partition stream by campaign_id for campaign aggregates.
- Use separate topics for impression/click/conversion due to different volume and correctness needs.
- Store lake data by event_date and event_type.
- Cluster by campaign_id/advertiser_id.
- Use OLAP store for advertiser dashboard slicing.

## 13. Consistency And Correctness

- Live dashboard can be near-real-time and slightly approximate.
- Billing must be reconciled and auditable.
- Deduplicate by impression_id, click_id, conversion_id.
- Late conversions update attribution windows.
- Spend should be idempotent to avoid overbilling.

## 14. Failure Handling

| Failure | Handling |
|---|---|
| duplicate click | dedupe by click_id |
| conversion arrives late | update attribution windows |
| stream lag | pacing uses stale metrics and alerts fire |
| bad campaign config | validate against campaign registry |
| OLAP serving down | dashboard degrades, billing pipeline continues |

## 15. Monitoring, Cost, And Security

Monitor:

- impression/click/conversion rates
- stream lag
- campaign spend freshness
- dashboard latency
- invalid traffic rate
- billing reconciliation mismatch

Cost:

- impressions are high volume; compress and partition
- pre-aggregate campaign metrics
- retain raw click/conversion longer than low-value debug details if needed

Security:

- avoid raw personal identifiers
- enforce advertiser data isolation
- audit billing/report access
- apply consent rules for tracking

## 16. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| real-time aggregation | fresh dashboards and pacing | streaming complexity |
| batch reconciliation | billing accuracy | delayed final numbers |
| detailed event logging | strong attribution | cost and privacy risk |
| approximate live metrics | fast and cheap | advertisers may see changing numbers |

## 17. Interview-Ready Final Answer

"I would design ad analytics with separate event streams for impressions, clicks, and conversions. Stream processing dedupes and computes campaign-level minute metrics for real-time dashboards and spend pacing. Raw events land in a lakehouse, where batch jobs reconcile billing, invalid traffic, and attribution windows. I would serve advertiser dashboards from an OLAP store and official reports from warehouse/lakehouse gold tables. The key concerns are dedupe, late conversions, billing correctness, invalid traffic, advertiser isolation, and separating live approximate metrics from finalized billing-grade metrics."

## 18. Quick Recall

- One-line summary: Ad analytics is real-time campaign scorekeeping plus billing reconciliation.
- Core tools: ad server events, Kafka, stream aggregation, OLAP, lakehouse, warehouse.
- Main trap: using live approximate numbers for final billing.
- Memory trick: advertiser scoreboard with a billing ledger.

