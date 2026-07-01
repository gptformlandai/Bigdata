# Topic 230: Access Control In Data Lakes

## 1. Goal

Understand how access control works when data lives in object storage and lakehouse tables.

## 2. Baby Intuition

A data lake is a huge storage building.

Access control decides which rooms, shelves, boxes, and files each person or job can use.

## 3. What It Is

- Simple definition: Data lake access control restricts who can read, write, or manage lake data.
- Technical definition: Access control in data lakes combines cloud IAM, storage policies, ACLs, table/catalog permissions, fine-grained controls, encryption keys, and audit logs to protect files and tables.
- Category: Data lake security.
- Related terms: bucket policy, ACL, IAM role, catalog permission, table format, lakehouse, Ranger, Lake Formation, Unity Catalog.

## 4. Why It Exists

Data lakes often contain:

- raw PII/PHI
- logs
- events
- curated marts
- ML features
- partner files
- archived data

Without access control, raw sensitive data can be copied, queried, or changed by the wrong users/jobs.

## 5. Where It Fits In A Data Platform

```text
object storage paths
  + table/catalog permissions
  + compute job identities
  + audit logs
  -> controlled lake access
```

## 6. How It Works Step By Step

1. Organize data into zones/domains.
2. Classify sensitive data.
3. Define storage-level permissions.
4. Define catalog/table-level permissions.
5. Configure compute job roles.
6. Apply row/column controls if supported.
7. Encrypt and restrict key access.
8. Audit access and policy changes.

## 7. How To Use It Practically

Layered controls:

| Layer | Example |
|---|---|
| storage | read/write path permissions |
| catalog | table/database grants |
| table | SELECT/INSERT/MERGE permissions |
| row | region-based filters |
| column | hide/mask PII columns |
| key | allow decrypt only to approved roles |
| network | private endpoint/VPC controls |

Good lake zones:

```text
bronze/raw: restricted
silver/clean: controlled domain access
gold/curated: broad approved BI access
```

## 8. Real-World Scenario

- Product/system: Enterprise S3/ADLS/GCS data lake.
- Problem: Raw customer files include PII, but product analysts only need curated aggregates.
- How access control helps: raw paths are restricted; curated gold tables are exposed through warehouse/lakehouse permissions.
- What would go wrong without it: users bypass curated tables and query raw PII files.

## 9. System Design Angle

Mention lake access control when:

- object storage is used as data lake
- multiple engines access same data
- raw and curated zones exist
- PII/PHI is stored
- catalog and storage permissions can drift

Important:

```text
Control both the files and the table metadata.
```

## 10. Trade-offs

| Strong Controls | Trade-off |
|---|---|
| safer raw data | more access management |
| clear zones | more architecture discipline |
| fine-grained permissions | tool compatibility complexity |
| encrypted data/key controls | more operational setup |

## 11. Failure Modes

- Failure: Table denied but storage path open.
- Symptom: user bypasses catalog and reads raw files.
- Recovery: restrict storage path.
- Prevention: align storage and catalog permissions.

- Failure: Write access too broad.
- Symptom: accidental overwrite/delete.
- Recovery: restore from version/snapshot/backups.
- Prevention: separate read/write/admin roles.

- Failure: Key policy too broad.
- Symptom: encrypted data readable by too many roles.
- Recovery: tighten KMS/key policy.
- Prevention: key access reviews.

## 12. Common Mistakes

- Mistake: Securing only the warehouse view.
- Why it is wrong: data may still be readable in object storage.
- Better approach: enforce layered lake, catalog, and compute access.

- Mistake: Using one bucket/container for everything with broad access.
- Why it is wrong: raw sensitive and curated data need different controls.
- Better approach: zone and classify data.

## 13. Mini Example

```text
raw/customers/:
  only ingestion and privacy-approved roles

silver/customers/:
  data engineering roles

gold/customer_metrics/:
  BI analyst roles
```

## 14. Interview Questions

1. How do you secure a data lake?
2. Storage permission vs catalog permission?
3. Why separate raw and curated zones?
4. What is bypass risk?
5. How do encryption keys fit lake access?

## 15. Interview Speak

"Data lake access control must be layered. I would protect object storage paths, catalog/table permissions, compute identities, encryption keys, row/column controls, and audit logs. A common mistake is securing only the table/view while leaving raw files readable."

## 16. Quick Recall

- One-line summary: Lake access control protects both files and table metadata.
- Three keywords: zones, catalog, storage.
- One trap: Catalog denied but raw path open.
- One memory trick: Lock rooms and the index cards.
