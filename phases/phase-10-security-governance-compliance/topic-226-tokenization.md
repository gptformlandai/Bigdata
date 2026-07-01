# Topic 226: Tokenization

## 1. Goal

Understand tokenization as replacing sensitive values with safe-looking tokens.

## 2. Baby Intuition

Tokenization swaps a real value for a placeholder.

```text
real email -> token_abc123
```

The token can be used for joins or tracking without exposing the original value.

## 3. What It Is

- Simple definition: Tokenization replaces sensitive data with tokens.
- Technical definition: Tokenization substitutes sensitive values with non-sensitive surrogate values, while the mapping to original values is stored separately in a protected token vault or controlled service.
- Category: Data protection and pseudonymization.
- Related terms: token vault, pseudonymization, surrogate key, detokenization, encryption, masking.

## 4. Why It Exists

Many analytics tasks need stable identity linkage but not raw identifiers.

Tokenization helps:

- join customer events without exposing email
- analyze claims without member ID
- share data with lower-risk identifiers
- reduce exposure in downstream systems
- limit access to original sensitive values

## 5. Where It Fits In A Data Platform

```text
raw sensitive identifier
  -> tokenization service
  -> token stored in analytics tables
  -> original mapping protected separately
```

## 6. How It Works Step By Step

1. Sensitive value enters pipeline.
2. Tokenization service generates or looks up token.
3. Analytics table stores token instead of raw value.
4. Token remains stable for joins if configured that way.
5. Only approved services/users can detokenize.
6. Token vault access is audited.

## 7. How To Use It Practically

Tokenization patterns:

| Pattern | Use |
|---|---|
| deterministic token | same input gets same token, useful for joins |
| random token | stronger unlinkability, needs vault lookup |
| format-preserving token | looks like original format where needed |
| one-way hash-like token | no detokenization, but careful with attacks |

Important:

```text
Tokenization quality depends on vault security and token design.
```

## 8. Real-World Scenario

- Product/system: Healthcare analytics lake.
- Problem: Analysts need to count unique members over time but should not see member IDs.
- How tokenization helps: member IDs become stable member tokens; raw IDs stay in restricted vault.
- What would go wrong without it: raw identifiers spread into many analytics tables.

## 9. System Design Angle

Use tokenization when:

- stable joins are needed
- raw identifiers should be hidden
- sensitive values appear in many downstream datasets
- controlled detokenization is required

Be careful with:

- token vault availability
- token collision risk
- reversible vs irreversible design
- brute-force attacks on predictable identifiers
- access to detokenization

## 10. Trade-offs

| Pros | Cons |
|---|---|
| reduces raw identifier exposure | token vault complexity |
| preserves joins if deterministic | tokens may still be sensitive |
| supports controlled detokenization | key/vault security critical |
| useful for sharing | re-identification risk remains with context |

## 11. Failure Modes

- Failure: Token vault compromised.
- Symptom: original sensitive values exposed.
- Recovery: incident response and rotate/re-tokenize where possible.
- Prevention: strict vault access and audit.

- Failure: Token not stable when needed.
- Symptom: joins break.
- Recovery: retokenize with deterministic strategy.
- Prevention: design token requirements up front.

- Failure: Tokens treated as non-sensitive.
- Symptom: tokens broadly shared and can be linked.
- Recovery: reclassify and restrict.
- Prevention: classify tokens based on risk.

## 12. Common Mistakes

- Mistake: Using simple unsalted hashes for low-cardinality identifiers.
- Why it is wrong: attackers may reverse by guessing.
- Better approach: use secure tokenization or keyed hashing.

- Mistake: Allowing many users to detokenize.
- Why it is wrong: raw data exposure returns.
- Better approach: restrict and audit detokenization.

## 13. Mini Example

```text
Raw:
email = aravind@example.com

Tokenized:
customer_token = tok_9f81a7

Analytics joins use customer_token.
Only approved service can map token back to email.
```

## 14. Interview Questions

1. What is tokenization?
2. Tokenization vs masking?
3. What is a token vault?
4. Why can tokens still be sensitive?
5. How does deterministic tokenization help joins?

## 15. Interview Speak

"Tokenization replaces sensitive values with surrogate tokens, keeping the mapping in a protected vault or service. It is useful when analytics needs stable identifiers for joins but should not expose raw PII/PHI. Detokenization must be tightly controlled and audited."

## 16. Quick Recall

- One-line summary: Tokenization swaps sensitive values for controlled tokens.
- Three keywords: token, vault, detokenization.
- One trap: Treating tokens as harmless.
- One memory trick: Use a badge number instead of the real name.
