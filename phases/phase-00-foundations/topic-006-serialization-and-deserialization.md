# Topic 006: Serialization And Deserialization

## Goal

Understand how programs convert in-memory objects into storable/transmittable bytes and back.

## Simple Explanation

Serialization means packing an object so it can be saved or sent.

Deserialization means unpacking it back into an object.

Example:

```text
Python dict -> JSON bytes -> network/file -> Python dict
```

## Core Idea

- Definition: Serialization converts data structures into a byte or text representation; deserialization reconstructs them.
- Why it matters: Systems cannot send a live object over a network. They send bytes.
- Related terms: JSON, Avro, Protobuf, schema, encoding, parsing, compatibility.

## How It Is Used

Serialization happens when:

- an API returns JSON
- a Kafka producer sends an Avro event
- Spark writes Parquet
- a service sends Protobuf over gRPC
- a database stores a record

Deserialization happens when:

- a consumer reads a Kafka message
- an API client parses JSON
- a Spark job reads files
- an application reads a database value

## Big Data / System Design Angle

At scale, serialization affects:

- message size
- CPU usage
- compatibility between producers and consumers
- schema evolution
- failure behavior when data is malformed

Common choices:

- JSON: easy to debug, larger, weaker type safety.
- Avro: compact, schema-driven, strong for data pipelines.
- Protobuf: compact, schema-driven, common in service communication.
- Parquet: columnar storage serialization for analytics.

## Example

```python
import json


event = {
    "event_id": "e1",
    "user_id": "u1",
    "event_type": "click",
}

serialized = json.dumps(event).encode("utf-8")
print(serialized)

deserialized = json.loads(serialized.decode("utf-8"))
print(deserialized["event_type"])
```

Output:

```text
b'{"event_id": "e1", "user_id": "u1", "event_type": "click"}'
click
```

## Common Mistakes

- Mistake: Assuming all consumers can read any serialized data.
- Better way: Agree on format and schema.

- Mistake: Ignoring backward and forward compatibility.
- Better way: Version schemas and evolve fields safely.

- Mistake: Using JSON for very high-throughput pipelines without checking cost.
- Better way: Consider Avro or Protobuf when size and CPU matter.

## Interview Speak

"Serialization is how systems convert records into bytes for storage or network transfer. In Big Data, I care about serialization because it affects message size, CPU cost, schema compatibility, and whether downstream consumers can safely read old and new versions of events."

## Quick Recall

- One-liner: Serialization packs data; deserialization unpacks it.
- Keywords: bytes, schema, compatibility.
- Trap: Forgetting that changing serialized data can break consumers.
