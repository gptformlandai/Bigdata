# Topic 214: Encryption At Rest And In Transit

## 1. Goal

Understand the two major encryption states for cloud data platforms.

## 2. Baby Intuition

Encryption at rest protects stored data.

Encryption in transit protects data while it moves.

Think locked warehouse and armored truck.

## 3. What It Is

- Simple definition: Encryption protects data by making it unreadable without keys.
- Technical definition: Encryption at rest protects stored data on disks/object storage/databases, while encryption in transit protects data moving over networks using protocols such as TLS.
- Category: Data security.
- Related terms: TLS, HTTPS, KMS, key, certificate, customer-managed key, server-side encryption.

## 4. Why It Exists

Data can be exposed if:

- disks/storage are compromised
- network traffic is intercepted
- backups are leaked
- logs contain sensitive payloads
- keys are poorly managed

Encryption reduces risk and is often required for compliance.

## 5. Where It Fits In A Data Platform

```text
storage buckets/databases/warehouses
  -> encryption at rest

client/job/service communication
  -> encryption in transit
```

Both matter.

## 6. How It Works Step By Step

At rest:

1. Data is written to storage.
2. Cloud service encrypts data before storing.
3. Encryption keys are managed by cloud provider or customer KMS.
4. Authorized reads decrypt data transparently.

In transit:

1. Client connects to service endpoint.
2. TLS/secure protocol is negotiated.
3. Data moves encrypted over network.
4. Receiver decrypts after secure transport.

## 7. How To Use It Practically

Data platform checklist:

- enable storage encryption
- use KMS/customer-managed keys when required
- rotate/manage keys carefully
- require HTTPS/TLS endpoints
- disable insecure protocols
- encrypt backups
- protect secrets
- audit key usage

Common examples:

```text
S3/ADLS/GCS encrypted at rest
JDBC/ODBC warehouse connections over TLS
Kafka/Event Hubs/Pub/Sub clients using encrypted transport
```

## 8. Real-World Scenario

- Product/system: Healthcare data lake.
- Problem: PHI must be protected in storage and while pipelines move it between services.
- How encryption helps: bucket/table data is encrypted at rest, and jobs connect over TLS; KMS controls key access.
- What would go wrong without it: leaked storage or intercepted traffic can expose sensitive data.

## 9. System Design Angle

Mention encryption when:

- PII/PHI/payment data exists
- cloud storage/warehouse is used
- compliance is required
- network communication crosses services
- key management is discussed

Maturity:

```text
Encryption is necessary but not sufficient; IAM, auditing, masking, and governance are also needed.
```

## 10. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| provider-managed keys | simpler | less key control |
| customer-managed keys | stronger control/audit | operational responsibility |
| strict TLS everywhere | safer network traffic | certificate/config management |
| key rotation | reduces exposure | can break jobs if mishandled |

## 11. Failure Modes

- Failure: Key disabled/deleted.
- Symptom: data cannot be decrypted/read.
- Recovery: restore key if possible.
- Prevention: key deletion guardrails.

- Failure: Client uses insecure endpoint.
- Symptom: data may move unencrypted.
- Recovery: enforce TLS.
- Prevention: network/security policies.

- Failure: Over-broad key access.
- Symptom: users can decrypt data they should not.
- Recovery: tighten KMS policy.
- Prevention: least privilege and audits.

## 12. Common Mistakes

- Mistake: Thinking encryption replaces access control.
- Why it is wrong: authorized users can still decrypt/read data.
- Better approach: combine encryption with IAM and governance.

- Mistake: Ignoring key management.
- Why it is wrong: losing/misconfiguring keys can break access.
- Better approach: manage keys with policy, rotation, backup, and audit.

## 13. Mini Example

```text
At rest:
S3 object stored encrypted with KMS key

In transit:
Spark job reads S3 over HTTPS/TLS
```

## 14. Interview Questions

1. Encryption at rest vs in transit?
2. What is KMS?
3. Provider-managed vs customer-managed keys?
4. Does encryption replace IAM?
5. What happens if a key is deleted?

## 15. Interview Speak

"Encryption at rest protects stored data, while encryption in transit protects data moving between clients and services, usually with TLS. In a data platform, I would enable storage encryption, use KMS/customer-managed keys where required, enforce TLS, audit key usage, and still rely on IAM and governance for access control."

## 16. Quick Recall

- One-line summary: At rest protects stored data; in transit protects moving data.
- Three keywords: TLS, KMS, keys.
- One trap: Thinking encryption alone solves security.
- One memory trick: Locked warehouse and armored truck.
