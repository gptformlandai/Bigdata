# Topic 053: Load Balancing

## Goal

Understand how load balancers distribute traffic across multiple servers for scale and availability.

## Simple Explanation

A load balancer is a traffic director.

It receives requests and sends them to healthy backend servers.

## Core Idea

- Definition: Load balancing distributes requests or work across multiple nodes.
- Why it matters: It improves availability, capacity, and fault isolation.
- Related terms: round robin, least connections, health check, sticky session, L4, L7.

## Common Algorithms

| Algorithm | How It Works | Best For |
|---|---|---|
| Round robin | rotate through servers | similar servers and requests |
| Least connections | choose fewest active connections | variable request duration |
| Weighted | send more to stronger servers | mixed capacity |
| Consistent hashing | route same key to same node | caches, sticky data |
| Random | choose random healthy node | simple distribution |

## Layer 4 vs Layer 7

Layer 4:

- routes by IP/port
- faster and simpler
- does not inspect HTTP details deeply

Layer 7:

- routes by HTTP path, headers, host
- supports smarter routing
- more processing overhead

## Big Data / System Design Angle

Load balancing appears in:

- API gateways
- service frontends
- query engines
- Kafka clients/brokers indirectly through partition routing
- distributed cache clients
- worker queues

Good load balancing requires:

- health checks
- failure detection
- connection draining
- timeouts
- retry policy
- avoiding overloaded backends

## Common Mistakes

- Mistake: Routing to unhealthy nodes.
- Better way: use health checks and remove bad nodes quickly.

- Mistake: Ignoring sticky state.
- Better way: make services stateless or use sticky sessions/consistent hashing when needed.

- Mistake: Retrying at multiple layers without coordination.
- Better way: avoid retry amplification.

## Interview Speak

"Load balancing spreads traffic across healthy nodes for scale and availability. I would choose an algorithm based on workload, use health checks, timeouts, and connection draining, and keep services stateless when possible. If requests depend on cached or partitioned data, I might use consistent hashing."

## Quick Recall

- One-liner: Load balancers spread work across healthy nodes.
- Keywords: health check, round robin, L7.
- Trap: Load balancing stateful services as if they were stateless.
