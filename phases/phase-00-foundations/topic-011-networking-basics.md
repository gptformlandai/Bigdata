# Topic 011: Networking Basics: HTTP, TCP, DNS, Ports

## Goal

Understand the basic networking concepts needed to reason about APIs, data movement, distributed systems, and production failures.

## Simple Explanation

Networking is how machines talk to each other.

When one service calls another, it needs:

- a name or address
- a protocol
- a port
- a reliable way to send bytes

## Core Idea

- Definition: Networking is communication between computers over agreed protocols.
- Why it matters: Data systems are distributed; data constantly moves between services, databases, queues, object stores, and clients.
- Related terms: IP, DNS, TCP, HTTP, TLS, port, request, response, timeout.

## Key Concepts

| Concept | Simple Meaning | Example |
|---|---|---|
| DNS | turns names into IP addresses | `api.company.com` -> `10.1.2.3` |
| IP address | machine/network address | `192.168.1.10` |
| Port | door into a process | PostgreSQL often uses `5432` |
| TCP | reliable byte stream | retries packets, preserves order |
| HTTP | request/response protocol | REST APIs |
| TLS | encryption in transit | HTTPS |

## How It Is Used

Data engineers encounter networking when:

- calling APIs
- connecting to databases
- producing to Kafka
- reading from cloud object storage
- configuring Airflow connections
- debugging timeouts
- setting firewall/security group rules

## Big Data / System Design Angle

Distributed systems fail through networks all the time.

Common failure patterns:

- DNS resolution fails
- connection refused
- port blocked
- TLS certificate issue
- timeout
- retry storm
- partial network partition
- slow network causing backpressure

Important design ideas:

- set timeouts
- use retries with backoff
- make writes idempotent
- monitor latency and error rates
- secure data in transit with TLS

## Example

HTTP request:

```text
Client -> DNS lookup -> TCP connection -> TLS handshake -> HTTP request -> HTTP response
```

API URL:

```text
https://api.example.com:443/orders
```

Breakdown:

- `https`: protocol
- `api.example.com`: host name
- `443`: port
- `/orders`: path

## Common Mistakes

- Mistake: Retrying forever on network errors.
- Better way: Use bounded retries with exponential backoff.

- Mistake: No timeouts.
- Better way: Always configure connection and request timeouts.

- Mistake: Treating network calls as guaranteed.
- Better way: Design for partial failure.

## Interview Speak

"In distributed data systems, networking is part of the design. Services communicate over protocols like HTTP or TCP, names are resolved through DNS, and processes listen on ports. I would handle network unreliability with timeouts, retries with backoff, idempotency, monitoring, and secure transport."

## Quick Recall

- One-liner: Networking is how distributed systems move bytes between machines.
- Keywords: DNS, TCP, HTTP, ports.
- Trap: Designing as if network calls cannot fail.
