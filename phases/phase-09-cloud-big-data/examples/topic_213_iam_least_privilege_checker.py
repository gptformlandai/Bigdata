REQUIRED_ACTIONS = {
    "read_raw_orders",
    "write_silver_orders",
    "start_etl_job",
}


def check_policy(allowed_actions):
    extra = allowed_actions - REQUIRED_ACTIONS
    missing = REQUIRED_ACTIONS - allowed_actions

    if not extra and not missing:
        return "least-privilege policy"

    messages = []
    if missing:
        messages.append(f"missing={sorted(missing)}")
    if extra:
        messages.append(f"extra={sorted(extra)}")

    return ", ".join(messages)


def main():
    policies = {
        "good_job_role": {
            "read_raw_orders",
            "write_silver_orders",
            "start_etl_job",
        },
        "too_broad_role": {
            "read_raw_orders",
            "write_silver_orders",
            "start_etl_job",
            "delete_bucket",
            "read_all_pii",
        },
        "broken_role": {
            "read_raw_orders",
        },
    }

    for role, actions in policies.items():
        print(f"{role}: {check_policy(actions)}")


if __name__ == "__main__":
    main()
