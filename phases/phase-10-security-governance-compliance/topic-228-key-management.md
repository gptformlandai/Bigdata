# Topic 228: Key Management

## 1. Goal

Understand key management as controlling the cryptographic keys used to protect data.

## 2. Baby Intuition

Encryption is the lock.

Key management is how you create, store, rotate, audit, and protect the keys.

## 3. What It Is

- Simple definition: Key management controls encryption keys.
- Technical definition: Key management is the lifecycle process for creating, storing, rotating, using, auditing, disabling, and destroying cryptographic keys.
- Category: Cryptographic operations and security governance.
- Related terms: KMS, CMK, key rotation, envelope encryption, HSM, key policy, key access.

## 4. Why It Exists

Encryption is only as strong as key control.

Bad key management can cause:

- unauthorized decryption
- permanent data loss
- compliance gaps
- inability to rotate after compromise
- unclear audit trail

## 5. Where It Fits In A Data Platform

```text
storage/warehouse/database/pipeline
  -> uses encryption key
  -> KMS/HSM controls key access
  -> audit logs record use
```

## 6. How It Works Step By Step

1. Create key in KMS/HSM.
2. Define key policy and allowed users/services.
3. Services encrypt/decrypt data using key.
4. Key usage is logged.
5. Key is rotated according to policy.
6. Old key versions remain for decrypting old data where needed.
7. Key may be disabled or retired safely.

## 7. How To Use It Practically

Good practices:

- use managed KMS/HSM
- restrict key administrators
- separate key users from key admins
- enable key usage logs
- rotate keys as required
- protect deletion with waiting periods/approvals
- separate keys by data domain/sensitivity when needed
- document ownership

Common key types:

| Type | Meaning |
|---|---|
| provider-managed key | cloud provider manages key lifecycle |
| customer-managed key | organization controls key policy/lifecycle |
| HSM-backed key | key protected by hardware security module |
| data key | key used to encrypt data directly |
| master/wrapping key | key used to encrypt data keys |

## 8. Real-World Scenario

- Product/system: PHI data lake.
- Problem: Sensitive raw claims need encryption with auditable customer-controlled keys.
- How key management helps: KMS key policies restrict decrypt to approved pipelines; usage is logged.
- What would go wrong without it: too many identities can decrypt PHI or keys may be deleted accidentally.

## 9. System Design Angle

Mention key management when:

- encryption is discussed
- sensitive data exists
- customer-managed keys are required
- compliance/audit matters
- cross-account/project access exists

Key phrase:

```text
Protecting the key is as important as encrypting the data.
```

## 10. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| provider-managed keys | simple | less control |
| customer-managed keys | control and audit | operational responsibility |
| frequent rotation | limits exposure | operational complexity |
| separate domain keys | smaller blast radius | more keys to manage |

## 11. Failure Modes

- Failure: Key deleted.
- Symptom: encrypted data unreadable.
- Recovery: restore if deletion window allows.
- Prevention: deletion protection and approval.

- Failure: Over-broad key policy.
- Symptom: unauthorized decrypt risk.
- Recovery: restrict key usage.
- Prevention: least privilege and reviews.

- Failure: No key usage audit.
- Symptom: cannot investigate decrypt activity.
- Recovery: enable logs.
- Prevention: audit-by-default.

## 12. Common Mistakes

- Mistake: Giving the same broad key to every dataset.
- Why it is wrong: one key compromise affects too much.
- Better approach: separate keys by domain/sensitivity where justified.

- Mistake: Rotating keys without testing.
- Why it is wrong: jobs may fail to decrypt data.
- Better approach: test rotation and rollback procedures.

## 13. Mini Example

```text
Key: pii-raw-zone-key
Can decrypt:
  pii-ingestion-service
  approved-privacy-admin
Cannot decrypt:
  general-analyst-role
```

## 14. Interview Questions

1. What is key management?
2. Provider-managed vs customer-managed keys?
3. Why rotate keys?
4. What happens if a key is deleted?
5. How do you restrict decrypt access?

## 15. Interview Speak

"Key management controls the lifecycle and access to encryption keys. I would use managed KMS/HSM, least-privilege key policies, separation of key admin and key usage, rotation, deletion guardrails, and audit logs because encryption is only useful if keys are protected."

## 16. Quick Recall

- One-line summary: Key management protects the keys that protect data.
- Three keywords: KMS, rotation, key policy.
- One trap: Deleting a key without recovery.
- One memory trick: Guard the key to the lock.
