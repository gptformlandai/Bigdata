# Big Data MAANG Mentorship Notes

This workspace is organized as a modular Big Data learning track: from baby-beginner foundations to MAANG-level data engineering and system design.

The goal is not just to memorize tools. The goal is to understand:

- what each concept is
- why it exists
- how it works internally
- when to use it
- when not to use it
- how it appears in real systems
- how to explain it in interviews
- how to reason about trade-offs, failures, and scale

## How To Study

Use one phase at a time, then one topic inside that phase.

1. Read the intuition first.
2. Read the definition and say it aloud in your own words.
3. Study how it works with the flow and code.
4. Focus on trade-offs and failure modes.
5. Practice the interview question.
6. Review the revision notes the next day.

After every 5 topics, review:

- a quiz
- a practical exercise
- a mini system design question
- a recap table

After every phase, review:

- phase summary
- must-know concepts
- common interview questions
- hands-on project
- production checklist

## Repository Structure

```text
.
+-- README.md
+-- ROADMAP.md
+-- TOPIC_TEMPLATE.md
+-- phases
    +-- phase-00-foundations
        +-- README.md
        +-- examples
            +-- topic_001_clickstream_simulation.py
        +-- phase-00-review.md
        +-- topic-001-what-is-data.md
        +-- topic-002-...
        +-- topic-020-horizontal-vs-vertical-scaling.md
    +-- phase-02-distributed-systems
        +-- README.md
        +-- examples
            +-- topic_043_consistent_hashing_demo.py
            +-- topic_050_retry_backoff_demo.py
        +-- phase-02-review.md
        +-- topic-040-distributed-systems.md
        +-- topic-041-...
        +-- topic-060-distributed-locks.md
```

## Current Progress

| Phase | Topics | Status |
|---|---:|---|
| Phase 0: Computer Science and Data Foundations | 001-020 | Complete |
| Phase 1: Big Data Basics | 021-039 | Not started |
| Phase 2: Distributed Systems Foundations | 040-060 | Complete |

## Next Topic

Phase 1, Topic 021: What is Big Data? Or continue forward to Phase 3, Topic 061: Hadoop overview.
