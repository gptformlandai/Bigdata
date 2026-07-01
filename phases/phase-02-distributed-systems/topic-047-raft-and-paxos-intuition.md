# Topic 047: Raft And Paxos Intuition

## Goal

Understand Raft and Paxos as consensus protocols at an intuition level.

## Simple Explanation

Raft and Paxos are ways for machines to agree on decisions even when some machines fail or messages are delayed.

Paxos is famous but hard to explain. Raft was designed to be easier to understand.

## Core Idea

- Definition: Paxos and Raft are consensus protocols for replicated state machines.
- Why it matters: They help distributed systems agree on a sequence of operations safely.
- Related terms: leader election, replicated log, majority, term, proposal, commit.

## Raft Intuition

Raft organizes consensus around a leader.

Main pieces:

- leader election
- log replication
- safety rules

Flow:

1. Nodes start as followers.
2. If no leader is heard from, a node becomes candidate.
3. Candidate asks for votes.
4. Majority vote makes it leader.
5. Leader accepts client commands.
6. Leader replicates log entries to followers.
7. Entry is committed after majority acknowledgement.

## Paxos Intuition

Paxos is more general and more abstract.

Main roles:

- proposers suggest values
- acceptors vote/accept proposals
- learners observe chosen values

The goal is to ensure only one value is chosen for a decision, even with failures.

## Big Data / System Design Angle

You do not usually implement Raft or Paxos yourself in interviews. You should know where they appear.

Used in:

- etcd
- ZooKeeper-style coordination
- Consul
- metadata stores
- leader election
- distributed locks
- replicated logs

Design rule:

```text
Use proven consensus systems instead of inventing your own.
```

## Raft vs Paxos

| Topic | Raft | Paxos |
|---|---|---|
| Understandability | easier | harder |
| Structure | leader-based | more abstract |
| Common use | practical systems | theory and some systems |
| Core goal | replicated log agreement | safe value agreement |

## Common Mistakes

- Mistake: Trying to hand-roll consensus.
- Better way: Use etcd, ZooKeeper, Consul, or managed primitives.

- Mistake: Thinking consensus keeps working with minority nodes.
- Better way: Consensus generally needs majority/quorum.

- Mistake: Using consensus for high-throughput data events unnecessarily.
- Better way: Use it for metadata, leader election, and coordination.

## Interview Speak

"Raft and Paxos are consensus protocols that help nodes agree on decisions despite failures. Raft is easier to reason about because it has leader election and log replication. In system design, I would usually rely on an existing consensus-backed system like etcd or ZooKeeper for leader election, metadata, or locks instead of implementing consensus myself."

## Quick Recall

- One-liner: Raft and Paxos are agreement protocols for distributed correctness.
- Keywords: leader, log, majority.
- Trap: Saying consensus works without quorum.
