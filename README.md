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

## Learning Style From Phase 1 Onward

Future phases move closer to real Big Data tools and platforms, so the notes should become more baby-step and practical.

For tool-driven topics, each note should explain:

- what it is in simple words
- why it exists
- what problem it solves
- where it fits in a data platform
- how it works step by step
- how to use it practically
- real-world scenarios
- system design trade-offs
- failure modes
- interview-ready language

Small supporting concepts can stay concise. Real tools like Hadoop, HDFS, Spark, Kafka, Hive, Flink, Airflow, Iceberg, Delta Lake, warehouses, and cloud services should get fuller treatment.

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
+-- AGENTS.md
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
    +-- phase-03-hadoop-ecosystem
        +-- README.md
        +-- examples
            +-- topic_064_hdfs_block_replication_calculator.py
            +-- topic_066_mapreduce_wordcount_simulation.py
        +-- phase-03-review.md
        +-- topic-061-hadoop-overview.md
        +-- topic-062-...
        +-- topic-077-why-spark-replaced-mapreduce-for-many-workloads.md
    +-- phase-04-spark-batch-processing
        +-- README.md
        +-- examples
            +-- topic_085_lazy_transformations_demo.py
            +-- topic_090_shuffle_simulation.py
            +-- topic_099_data_skew_demo.py
        +-- phase-04-review.md
        +-- topic-078-apache-spark-overview.md
        +-- topic-079-...
        +-- topic-106-spark-on-emr-dataproc-databricks.md
    +-- phase-05-streaming-messaging
        +-- README.md
        +-- examples
            +-- topic_112_kafka_partition_consumer_group_simulation.py
            +-- topic_121_delivery_semantics_simulation.py
            +-- topic_132_watermark_window_simulation.py
        +-- phase-05-review.md
        +-- topic-107-event-driven-architecture.md
        +-- topic-108-...
        +-- topic-137-real-time-analytics-architecture.md
    +-- phase-06-modern-data-lakehouse
        +-- README.md
        +-- examples
            +-- topic_143_snapshot_isolation_demo.py
            +-- topic_147_cow_vs_mor_simulation.py
            +-- topic_148_upsert_merge_demo.py
            +-- topic_150_partition_evolution_demo.py
        +-- phase-06-review.md
        +-- topic-138-data-lakehouse-architecture.md
        +-- topic-139-...
        +-- topic-154-lakehouse-performance-tuning.md
    +-- phase-07-warehouses-query-engines
        +-- README.md
        +-- examples
            +-- topic_165_columnar_pruning_demo.py
            +-- topic_166_mpp_aggregation_demo.py
            +-- topic_169_materialized_view_demo.py
            +-- topic_174_scd_type2_demo.py
        +-- phase-07-review.md
        +-- topic-155-data-warehouse-architecture.md
        +-- topic-156-...
        +-- topic-175-data-modeling-for-analytics.md
    +-- phase-08-orchestration-dataops
        +-- README.md
        +-- examples
            +-- topic_177_dag_topological_order_demo.py
            +-- topic_182_retry_backoff_demo.py
            +-- topic_189_data_contract_validator.py
            +-- topic_194_alert_severity_router.py
        +-- phase-08-review.md
        +-- topic-176-apache-airflow.md
        +-- topic-177-...
        +-- topic-195-incident-response-for-data-pipelines.md
    +-- phase-09-cloud-big-data
        +-- README.md
        +-- examples
            +-- topic_196_cloud_lake_path_builder.py
            +-- topic_200_stream_partition_demo.py
            +-- topic_212_query_scan_cost_demo.py
            +-- topic_213_iam_least_privilege_checker.py
        +-- phase-09-review.md
        +-- topic-196-aws-s3.md
        +-- topic-197-...
        +-- topic-215-vpc-networking-basics-for-data-platforms.md
    +-- phase-10-security-governance-compliance
        +-- README.md
        +-- examples
            +-- topic_217_authorization_policy_demo.py
            +-- topic_225_masking_tokenization_demo.py
            +-- topic_231_row_column_security_demo.py
            +-- topic_233_retention_policy_demo.py
        +-- phase-10-review.md
        +-- topic-216-authentication.md
        +-- topic-217-...
        +-- topic-235-governance-at-scale.md
```

## Current Progress

| Phase | Topics | Status |
|---|---:|---|
| Phase 0: Computer Science and Data Foundations | 001-020 | Complete |
| Phase 1: Big Data Basics | 021-039 | Not started |
| Phase 2: Distributed Systems Foundations | 040-060 | Complete |
| Phase 3: Hadoop Ecosystem | 061-077 | Complete |
| Phase 4: Spark And Batch Processing | 078-106 | Complete |
| Phase 5: Streaming And Messaging | 107-137 | Complete |
| Phase 6: Modern Data Lakehouse | 138-154 | Complete |
| Phase 7: Warehouses And Query Engines | 155-175 | Complete |
| Phase 8: Orchestration And DataOps | 176-195 | Complete |
| Phase 9: Cloud Big Data | 196-215 | Complete |
| Phase 10: Security, Governance, And Compliance | 216-235 | Complete |

## Next Topic

Phase 11, Topic 236: Lambda architecture. Phase 1 is still available if you want to fill the skipped Big Data basics.
