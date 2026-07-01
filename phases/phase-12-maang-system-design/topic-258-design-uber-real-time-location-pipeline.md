# Topic 258: Design Uber Real-Time Location Pipeline

## 1. Goal

Design a pipeline that ingests driver/rider location updates and supports matching, ETA, surge, live maps, and analytics.

## 2. Baby Intuition

Uber-like systems are built around moving dots.

The platform must constantly answer:

```text
where are drivers now,
which drivers are near a rider,
how long will pickup take,
and what is demand/supply in each area?
```

## 3. Requirements

Clarify:

- Are we designing real-time dispatch or analytics only?
- How fresh must driver locations be?
- What location precision is required?
- Do we need historical trip analytics?
- Which cities/regions are in scope?

## 4. Functional Requirements

- ingest driver and rider location updates
- maintain latest driver location state
- query nearby available drivers
- compute supply/demand by region
- publish real-time updates to dispatch and maps
- store historical location/trip data for analytics
- detect stale or invalid locations

## 5. Non-Functional Requirements

- very low latency for latest location
- high write throughput
- high availability
- geospatial partitioning
- privacy and retention controls
- graceful handling of mobile disconnects
- regional isolation for compliance/latency

## 6. Capacity Estimation

Example:

```text
5M active drivers globally
location update every 4 seconds
= 1.25M updates/sec peak if all active

event size about 300 bytes
= about 375 MB/sec before replication/compression
```

Even if actual active drivers are lower, design must handle city-level peaks and events during busy hours.

## 7. Events And APIs

Location update:

```json
{
  "driver_id": "d1",
  "lat": 37.7749,
  "lon": -122.4194,
  "heading": 90,
  "speed_mps": 8.5,
  "status": "available",
  "event_time": "2026-07-02T10:00:00Z"
}
```

Key APIs:

```text
POST /location/driver
GET /nearby-drivers?lat=...&lon=...&radius=...
```

## 8. Data Model

Latest location store:

```text
driver_latest_location
- driver_id
- geocell
- lat
- lon
- status
- event_time
- expires_at
```

Historical lake table:

```text
driver_location_events(event_date, city_id, driver_id_hash, geocell, lat, lon, speed, event_time)
```

Regional aggregate:

```text
geocell_supply_demand(window_start, geocell, available_drivers, ride_requests, surge_signal)
```

## 9. High-Level Architecture

```text
driver/rider apps
  -> location gateway
  -> Kafka/Pub/Sub partitioned by city/geocell
  -> stream processor
  -> latest location store/geospatial index
  -> dispatch, ETA, maps

stream/lake sink
  -> historical lakehouse
  -> batch analytics, demand forecasting, ML features
```

## 10. Data Flow

1. Driver app sends location every few seconds.
2. Gateway validates auth, timestamp, and reasonable movement.
3. Event is assigned to city and geocell.
4. Stream processor updates latest driver state.
5. Nearby-driver service queries geocells around rider.
6. Aggregation job computes supply/demand by geocell and time window.
7. Raw location history is stored for analytics and model training.

## 11. Deep Dive Components

Geospatial indexing:

- divide world into cells such as geohash/S2/H3 style regions
- store each driver's latest cell
- nearby query scans rider's cell plus neighboring cells
- larger radius means more neighboring cells

Freshness:

- driver location expires after short TTL
- stale drivers are removed from available pool
- out-of-order updates are ignored if older than current state

## 12. Scaling And Partitioning

- Partition streams by city_id and geocell.
- Keep dispatch data regional to reduce latency.
- Shard hot geocells in dense areas.
- Use TTL stores like Redis/Cassandra/DynamoDB for latest state.
- Store historical data partitioned by event_date and city_id.

## 13. Consistency And Correctness

- Latest location is eventually consistent but must be fresh.
- Ignore old updates using event_time or sequence number.
- For dispatch, freshness matters more than perfect history.
- For analytics, raw historical data should be complete and replayable.

## 14. Failure Handling

| Failure | Handling |
|---|---|
| driver offline | location expires by TTL |
| duplicate update | idempotent latest-state overwrite |
| out-of-order update | compare event_time/sequence |
| stream lag | degrade matching radius or use last known state |
| regional outage | fail over region if possible, with reduced freshness |

## 15. Monitoring, Cost, And Security

Monitor:

- location update rate by city
- latest-state freshness
- nearby query latency
- stale driver count
- stream lag
- invalid movement rate

Cost:

- keep latest store small with TTL
- compress historical data
- downsample old location history where allowed

Security:

- encrypt location data
- restrict access to precise location
- anonymize for analytics where possible
- enforce retention for location history

## 16. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| very frequent updates | better ETA/matching | battery and infrastructure cost |
| precise location retention | richer analytics | privacy risk |
| regional processing | low latency | operational duplication |
| geocell indexing | fast nearby lookup | boundary and hot-cell complexity |

## 17. Interview-Ready Final Answer

"I would design the location system around low-latency regional ingestion. Driver apps send authenticated location updates to a gateway, which assigns city and geocell and writes to Kafka. A stream processor updates a TTL-based latest-location store and geospatial index for dispatch. Nearby-driver queries scan the rider's geocell and neighbors. Raw events are also written to a lakehouse for analytics, demand forecasting, and ML. I would handle stale drivers with TTL, out-of-order events with timestamps or sequence numbers, hot cells with sharding, and location privacy with encryption, access control, anonymization, and retention limits."

## 18. Quick Recall

- One-line summary: Uber location design is fresh geospatial state plus historical analytics.
- Core tools: location gateway, Kafka, geocells, stream processor, TTL latest store, lakehouse.
- Main trap: using only batch storage for real-time driver matching.
- Memory trick: moving dots need fresh state.

