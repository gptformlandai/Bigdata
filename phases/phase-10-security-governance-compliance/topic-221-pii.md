# Topic 221: PII

## 1. Goal

Understand personally identifiable information and how data platforms should handle it.

## 2. Baby Intuition

PII is data that can identify a person.

Your name alone may identify you in some places. Your email, phone, government ID, or address can identify you even more clearly.

## 3. What It Is

- Simple definition: PII is information that identifies or can help identify a person.
- Technical definition: PII includes direct identifiers and combinations of indirect identifiers that can reasonably link data to an individual.
- Category: Sensitive data classification.
- Related terms: personal data, direct identifier, quasi-identifier, masking, tokenization, encryption, minimization.

## 4. Why It Exists

Companies collect personal data for real business needs:

- account creation
- billing
- support
- personalization
- compliance
- fraud prevention

But collecting personal data creates risk. If exposed or misused, it can harm people and create legal, financial, and trust damage.

## 5. Where It Fits In A Data Platform

```text
source systems
  -> PII fields detected/classified
  -> protected in lake/warehouse/pipelines
  -> masked/tokenized/limited for users
  -> audited and retained/deleted by policy
```

## 6. How It Works Step By Step

1. Identify PII fields.
2. Classify sensitivity.
3. Define who needs access and why.
4. Minimize collection and copies.
5. Protect with access control, masking, tokenization, and encryption.
6. Log access.
7. Apply retention and deletion policy.
8. Monitor for leaks or policy violations.

## 7. How To Use It Practically

Common PII examples:

| Type | Example |
|---|---|
| direct identifier | name, email, phone |
| government identifier | SSN, passport, national ID |
| location | home address, precise GPS |
| online identifier | device ID, IP address, cookie ID |
| financial | bank account, card details |
| quasi-identifier | birth date plus ZIP code |

Practical controls:

- classify columns
- restrict raw access
- mask in BI
- tokenize identifiers
- encrypt storage
- avoid logging PII
- use purpose-based access where needed

## 8. Real-World Scenario

- Product/system: Customer analytics warehouse.
- Problem: Analysts need customer behavior trends but not raw email or phone numbers.
- How PII handling helps: raw PII stays restricted; analytics uses customer surrogate IDs and masked fields.
- What would go wrong without it: broad analyst access exposes sensitive customer data.

## 9. System Design Angle

Mention PII when:

- customer/user/member data is used
- data lake raw zone is discussed
- logs/events contain identifiers
- GDPR/CCPA/privacy is relevant
- deletion/retention/masking is required

Design:

```text
classify -> minimize -> protect -> monitor -> delete when required
```

## 10. Trade-offs

| Protection | Trade-off |
|---|---|
| masking | less detail for debugging |
| tokenization | token vault/lookup complexity |
| strict access | more approval workflow |
| minimization | some analytics use cases harder |
| shorter retention | less history for analysis |

## 11. Failure Modes

- Failure: PII in logs.
- Symptom: sensitive data spreads to logging systems.
- Recovery: scrub logs and rotate/delete where possible.
- Prevention: logging filters and reviews.

- Failure: PII copied into uncontrolled marts.
- Symptom: many teams can access sensitive data.
- Recovery: locate and restrict/delete copies.
- Prevention: classification and lineage.

- Failure: Unclear data ownership.
- Symptom: no one approves or reviews access.
- Recovery: assign data owner/steward.
- Prevention: governance metadata.

## 12. Common Mistakes

- Mistake: Thinking only SSN or passport is PII.
- Why it is wrong: emails, device IDs, IPs, and combinations can identify people.
- Better approach: classify both direct and indirect identifiers.

- Mistake: Keeping PII forever because storage is cheap.
- Why it is wrong: retention increases risk.
- Better approach: retain by policy and business purpose.

## 13. Mini Example

```text
Raw table:
customer_id, email, phone, address, signup_ts

Analytics table:
customer_key, region, signup_month, segment

Email/phone/address are removed or masked for general analytics.
```

## 14. Interview Questions

1. What is PII?
2. Direct identifier vs quasi-identifier?
3. How do you protect PII in a data lake?
4. Why should logs avoid PII?
5. Masking vs tokenization?

## 15. Interview Speak

"PII is information that identifies or can reasonably link to a person. In a data platform, I would classify PII, minimize copies, restrict raw access, mask or tokenize fields, encrypt storage and transport, audit access, and apply retention/deletion policies."

## 16. Quick Recall

- One-line summary: PII is data that can identify a person.
- Three keywords: classify, minimize, protect.
- One trap: PII leaking into logs and marts.
- One memory trick: If it points to a person, treat it carefully.
