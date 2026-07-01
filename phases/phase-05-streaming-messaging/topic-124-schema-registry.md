# Topic 124: Schema Registry

## 1. Goal

Understand Schema Registry as the place that stores and enforces event schemas.

## 2. Baby Intuition

Schema Registry is like a contract office.

Before producers send messages and consumers read them, everyone agrees on the format.

## 3. What It Is

- Simple definition: Schema Registry stores schemas for Kafka messages.
- Technical definition: Schema Registry is a service that manages schemas and compatibility rules for serialized data formats such as Avro, Protobuf, or JSON Schema.
- Category: Schema governance.
- Related terms: subject, schema version, compatibility, serializer, deserializer.

## 4. Why It Exists

Kafka stores bytes.

Consumers need to know:

- what fields exist
- what types fields have
- whether a schema change is safe
- how to deserialize bytes

Schema Registry prevents producers from breaking consumers accidentally.

## 5. Where It Fits In A Data Platform

```text
Producer serializer -> Schema Registry -> Kafka bytes -> Consumer deserializer
```

The registry is not usually in the hot data path for every message after schema is cached, but it is critical for schema lookup and validation.

## 6. How It Works Step By Step

1. Producer has a schema.
2. Serializer checks/registers schema in registry.
3. Registry validates compatibility.
4. Message is serialized with schema id.
5. Consumer reads message.
6. Deserializer uses schema id to fetch schema.
7. Consumer gets structured record.

## 7. How To Use It Practically

Compatibility modes:

```text
BACKWARD
FORWARD
FULL
NONE
```

Safe change example:

```text
add optional field with default
```

Breaking change example:

```text
rename required field
```

## 8. Real-World Scenario

- Product/system: Order event platform.
- Problem: Producer wants to add `coupon_code`.
- How Schema Registry helps: Allows change only if compatible.
- What would go wrong without it: consumers may fail parsing events.

## 9. System Design Angle

Schema Registry matters when:

- many teams share topics
- events are long-lived
- replay is needed
- schema evolution happens often
- data contracts matter

Design questions:

- who owns schema?
- what compatibility mode?
- how are breaking changes handled?
- how do consumers upgrade?

## 10. Trade-offs

| What We Gain | What We Pay |
|---|---|
| schema safety | registry dependency |
| compatibility checks | governance process |
| easier deserialization | schema versioning complexity |
| better contracts | producer discipline |

## 11. Failure Modes

- Failure: incompatible schema change.
- Symptom: producer rejected or consumers fail.
- Recovery: roll back or version topic/schema.
- Prevention: compatibility checks.

- Failure: registry unavailable.
- Symptom: producers/consumers may fail if schema not cached.
- Recovery: restore registry.
- Prevention: HA registry and caching.

## 12. Common Mistakes

- Mistake: Using JSON without schema for important events.
- Why it is wrong: schema drift breaks consumers.
- Better approach: use Schema Registry or contracts.

- Mistake: Deleting fields casually.
- Why it is wrong: old consumers may depend on them.
- Better approach: deprecate and migrate.

## 13. Mini Example

Schema evolution:

```text
v1: order_id, amount
v2: order_id, amount, currency default "USD"
```

This is usually backward compatible.

## 14. Interview Questions

1. What is Schema Registry?
2. Why does Kafka need schemas?
3. What is compatibility mode?
4. What schema changes are safe?
5. What happens if registry is down?

## 15. Interview Speak

"Schema Registry manages event schemas and compatibility rules for formats like Avro, Protobuf, and JSON Schema. It protects consumers from breaking producer changes and enables safe schema evolution. In shared Kafka platforms, it is a key part of data governance."

## 16. Quick Recall

- One-line summary: Schema Registry is the contract store for Kafka messages.
- Three keywords: schema, version, compatibility.
- One trap: Schema-free important events.
- One memory trick: Contract office for events.
