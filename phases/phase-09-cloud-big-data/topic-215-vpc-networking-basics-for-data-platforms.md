# Topic 215: VPC/Networking Basics For Data Platforms

## 1. Goal

Understand basic cloud networking concepts that matter for data platforms.

## 2. Baby Intuition

A VPC is like your private cloud office building.

Subnets are rooms/floors, security rules are doors, and private endpoints are secure hallways to cloud services.

## 3. What It Is

- Simple definition: Cloud networking controls how data services communicate securely.
- Technical definition: VPC/networking design uses private networks, subnets, routes, firewalls/security groups, private endpoints, NAT, peering, and connectivity controls to govern traffic between data services, users, and the internet.
- Category: Cloud networking and security foundation.
- Related terms: VPC, subnet, route table, security group, firewall, private endpoint, NAT, peering, VPN, Direct Connect/Interconnect/ExpressRoute.

## 4. Why It Exists

Data platforms need network controls because:

- data services must talk to storage/warehouses
- private data should not move over public internet unnecessarily
- jobs need access to databases
- external vendors may connect
- compliance may require network isolation
- egress costs and risks matter

## 5. Where It Fits In A Data Platform

```text
data jobs / clusters / warehouses
  -> private network/subnets
  -> private endpoints to storage/services
  -> controlled access to databases/APIs
  -> monitored egress
```

## 6. How It Works Step By Step

1. Create private network/VPC.
2. Split address space into subnets.
3. Place compute resources in subnets.
4. Configure routes.
5. Apply firewall/security group rules.
6. Use private endpoints/service endpoints where possible.
7. Control outbound internet through NAT/proxies.
8. Connect on-prem or other clouds through VPN/dedicated links if needed.
9. Monitor traffic and logs.

## 7. How To Use It Practically

Core concepts:

| Concept | Meaning |
|---|---|
| VPC/VNet | isolated cloud network |
| subnet | IP range inside network |
| route table | where traffic goes |
| security group/firewall | allowed traffic rules |
| private endpoint | private access to managed service |
| NAT | private resources reach internet outbound |
| peering | connect networks |
| VPN/dedicated link | connect on-prem to cloud |

## 8. Real-World Scenario

- Product/system: Secure healthcare data lake.
- Problem: Spark jobs must read storage and database data without exposing services publicly.
- How networking helps: jobs run in private subnets, use private endpoints to storage, and access databases through controlled rules.
- What would go wrong without it: sensitive systems may be reachable from public networks.

## 9. System Design Angle

Mention networking when:

- data services access private databases
- compliance/security is important
- cross-region/cloud/on-prem access exists
- managed services need private access
- egress cost matters

Strong phrase:

```text
Keep data-plane traffic private where possible and explicitly control ingress/egress.
```

## 10. Trade-offs

| More Private Networking | More Public/Simple Networking |
|---|---|
| stronger security | easier setup |
| lower exposure | faster experimentation |
| better compliance story | fewer networking tickets |
| more configuration | higher risk if misconfigured |

## 11. Failure Modes

- Failure: Security rule too strict.
- Symptom: pipeline cannot connect to database/storage.
- Recovery: add specific allowed route/port.
- Prevention: connectivity tests.

- Failure: Security rule too broad.
- Symptom: unnecessary exposure.
- Recovery: restrict CIDRs/ports.
- Prevention: least-privilege networking.

- Failure: Cross-region egress surprise.
- Symptom: high data transfer cost.
- Recovery: colocate data/compute.
- Prevention: architecture review for data movement.

## 12. Common Mistakes

- Mistake: Opening services to the public internet for convenience.
- Why it is wrong: increases attack surface.
- Better approach: use private endpoints, VPN, bastion, or controlled access.

- Mistake: Ignoring network egress in data design.
- Why it is wrong: moving large data across regions/clouds can be costly and slow.
- Better approach: process data near where it lives.

## 13. Mini Example

```text
Private Spark cluster subnet
  -> private endpoint to object storage
  -> firewall rule to database port
  -> no public inbound access
```

## 14. Interview Questions

1. What is a VPC/VNet?
2. What is a subnet?
3. What is a private endpoint?
4. Why avoid public access to data systems?
5. How can networking affect cloud cost?

## 15. Interview Speak

"For cloud data platforms, networking controls how compute, storage, databases, and users communicate. I would use private subnets, least-privilege firewall rules, private endpoints to managed services, controlled egress, and connectivity tests, while processing data near storage to reduce latency and transfer cost."

## 16. Quick Recall

- One-line summary: Cloud networking controls private, secure data movement.
- Three keywords: VPC, subnet, private endpoint.
- One trap: Public access for convenience.
- One memory trick: Private cloud office with locked doors.
