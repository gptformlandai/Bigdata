def build_resume_bullet(action, system, tools, outcome, engineering_detail):
    return (
        f"{action} {system} using {tools} to {outcome}, "
        f"with {engineering_detail}."
    )


def main():
    bullets = [
        build_resume_bullet(
            "Built",
            "an end-to-end clickstream analytics pipeline",
            "Kafka, Spark, and lakehouse tables",
            "produce product funnel metrics from simulated user events",
            "deduplication, sessionization, and late-event handling",
        ),
        build_resume_bullet(
            "Designed",
            "a MySQL CDC to lakehouse pipeline",
            "Debezium-style events, Kafka, and MERGE logic",
            "replicate inserts, updates, and deletes into analytics tables",
            "idempotent writes, schema handling, and source-target reconciliation",
        ),
    ]

    for bullet in bullets:
        print(f"- {bullet}")


if __name__ == "__main__":
    main()

