# Topic 227: Encryption

## 1. Goal

Understand encryption as a core way to protect data confidentiality.

## 2. Baby Intuition

Encryption locks data with a key.

Without the key, the data should look unreadable.

## 3. What It Is

- Simple definition: Encryption turns readable data into unreadable ciphertext using keys.
- Technical definition: Encryption uses cryptographic algorithms and keys to protect data confidentiality at rest, in transit, or sometimes at field/application level.
- Category: Cryptographic protection.
- Related terms: ciphertext, plaintext, key, KMS, TLS, envelope encryption, symmetric encryption, asymmetric encryption.

## 4. Why It Exists

Data may be exposed through:

- stolen storage media
- leaked backups
- network interception
- unauthorized file copies
- compromised logs/exports

Encryption reduces the value of exposed data if keys remain protected.

## 5. Where It Fits In A Data Platform

```text
data at rest:
  object storage, databases, warehouses, backups

data in transit:
  client to service, service to service, pipeline to warehouse

field/application level:
  specific sensitive values encrypted before storage
```

## 6. How It Works Step By Step

At a high level:

1. Plaintext data is created.
2. Encryption algorithm uses a key.
3. Output becomes ciphertext.
4. Ciphertext is stored or sent.
5. Authorized process uses key to decrypt.
6. Key access is logged and controlled.

## 7. How To Use It Practically

Common types:

| Type | Example |
|---|---|
| encryption at rest | S3/ADLS/GCS/warehouse storage encryption |
| encryption in transit | TLS/HTTPS/JDBC over TLS |
| field-level encryption | encrypt SSN column before storage |
| envelope encryption | data key encrypts data; master key encrypts data key |

Good practices:

- encrypt storage by default
- enforce TLS
- use managed KMS where possible
- rotate/manage keys
- restrict key access
- do not log plaintext secrets/PII

## 8. Real-World Scenario

- Product/system: Customer data lake.
- Problem: Raw customer files include emails and addresses.
- How encryption helps: files are encrypted at rest and jobs connect over TLS; key access is restricted.
- What would go wrong without it: leaked files/backups may expose readable data.

## 9. System Design Angle

Mention encryption when:

- sensitive data is stored or moved
- cloud storage/warehouse is used
- compliance is discussed
- backups/exports exist
- key management is required

Important:

```text
Encryption protects confidentiality, but access control decides who can decrypt/read.
```

## 10. Trade-offs

| Pros | Cons |
|---|---|
| protects data confidentiality | key management complexity |
| supports compliance | not a replacement for IAM |
| protects backups/storage | application-level encryption can limit querying |
| works across storage/network | performance/operational overhead can exist |

## 11. Failure Modes

- Failure: Key exposed.
- Symptom: encrypted data can be decrypted by attacker.
- Recovery: rotate keys and investigate.
- Prevention: KMS, least privilege, audits.

- Failure: Key deleted.
- Symptom: data becomes unreadable.
- Recovery: restore key if possible.
- Prevention: deletion protection and backups.

- Failure: Plaintext copied elsewhere.
- Symptom: encrypted source but unprotected export.
- Recovery: remove/secure export.
- Prevention: egress/export controls.

## 12. Common Mistakes

- Mistake: Saying "it is encrypted" and ignoring permissions.
- Why it is wrong: authorized identities can still read decrypted data.
- Better approach: combine encryption, IAM, audit, and masking.

- Mistake: Building custom crypto casually.
- Why it is wrong: cryptography is easy to implement incorrectly.
- Better approach: use proven libraries and managed KMS.

## 13. Mini Example

```text
S3 object:
stored as ciphertext

Spark job:
has role allowed to use KMS key
reads decrypted data through service

Unauthorized user:
cannot decrypt/read object
```

## 14. Interview Questions

1. What is encryption?
2. At rest vs in transit?
3. What is KMS?
4. Does encryption replace access control?
5. What happens if a key is deleted?

## 15. Interview Speak

"Encryption protects data confidentiality by making data unreadable without keys. In data platforms, I would use encryption at rest, TLS in transit, managed KMS, strict key access, and audit logging, while remembering encryption complements but does not replace IAM and governance."

## 16. Quick Recall

- One-line summary: Encryption locks data with keys.
- Three keywords: key, ciphertext, KMS.
- One trap: Ignoring who can decrypt.
- One memory trick: Locked data, guarded key.
