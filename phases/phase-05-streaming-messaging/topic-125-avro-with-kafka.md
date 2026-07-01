# Topic 125: Avro With Kafka

## 1. Goal

Understand why Avro is commonly used with Kafka and Schema Registry.

## 2. Baby Intuition

JSON is easy to read but bulky and loose.

Avro is compact and schema-aware, like a packed form that both sender and receiver understand.

## 3. What It Is

- Simple definition: Avro is a compact schema-based data format often used for Kafka events.
- Technical definition: Apache Avro is a binary serialization format that uses schemas to encode and decode records, supporting schema evolution.
- Category: Serialization format.
- Related terms: schema, serializer, deserializer, Schema Registry, compatibility.

## 4. Why It Exists

Kafka messages are bytes.

Teams need a format that is:

- compact
- typed
- schema-driven
- good for evolution
- language-neutral

Avro fits these needs well.

## 5. Where It Fits In A Data Platform

```text
Producer object -> Avro serializer -> Kafka bytes -> Avro deserializer -> Consumer object
```

Avro often works with Schema Registry.

## 6. How It Works Step By Step

1. Define Avro schema.
2. Producer uses Avro serializer.
3. Serializer registers/looks up schema id.
4. Record is encoded as compact bytes.
5. Kafka stores bytes.
6. Consumer deserializer reads schema id.
7. Consumer gets typed record.

## 7. How To Use It Practically

Example schema:

```json
{
  "type": "record",
  "name": "OrderCreated",
  "fields": [
    {"name": "order_id", "type": "string"},
    {"name": "amount", "type": "double"},
    {"name": "currency", "type": "string", "default": "USD"}
  ]
}
```

Safe evolution:

```text
add field with default
```

Risky evolution:

```text
change amount from double to string
```

## 8. Real-World Scenario

- Product/system: Payment events.
- Problem: Many services need compact, typed events with safe evolution.
- How Avro helps: Schema defines fields and binary encoding saves space.
- What would go wrong without it: JSON drift and larger messages increase risk/cost.

## 9. System Design Angle

Avro is useful when:

- Kafka throughput matters
- schema contracts matter
- events evolve over time
- multiple languages consume data

Trade-off:

```text
less human-readable than JSON, but safer and more compact
```

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| compact binary messages | not human-readable directly |
| schema evolution | schema governance needed |
| strong typing | serializer/deserializer setup |
| language-neutral | tooling dependency |

## 11. Failure Modes

- Failure: incompatible schema.
- Symptom: producer rejected or consumer decode fails.
- Recovery: fix schema.
- Prevention: compatibility rules.

- Failure: consumer lacks schema registry access.
- Symptom: deserialization fails.
- Recovery: restore access/config.
- Prevention: HA registry and cached schemas.

## 12. Common Mistakes

- Mistake: Adding required field without default.
- Why it is wrong: old records do not have that field.
- Better approach: add optional/defaulted fields.

- Mistake: Treating Avro bytes like readable JSON.
- Why it is wrong: Avro is binary.
- Better approach: use Avro tools/deserializers.

## 13. Mini Example

JSON:

```json
{"order_id":"o1","amount":10.5}
```

Avro:

```text
schema + compact binary payload
```

## 14. Interview Questions

1. Why use Avro with Kafka?
2. How does Avro support schema evolution?
3. Avro vs JSON?
4. Why do defaults matter?
5. How does Schema Registry fit?

## 15. Interview Speak

"Avro is a compact binary serialization format with explicit schemas. With Kafka and Schema Registry, it lets producers and consumers agree on event structure and evolve schemas safely. It is less human-readable than JSON but better for typed, high-throughput production event streams."

## 16. Quick Recall

- One-line summary: Avro is compact schema-based event serialization.
- Three keywords: binary, schema, evolution.
- One trap: Required new fields without defaults.
- One memory trick: Avro is a packed contract form.
