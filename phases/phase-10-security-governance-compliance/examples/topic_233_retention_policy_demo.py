from datetime import date


POLICIES = {
    "debug_logs": 30,
    "clickstream_raw": 395,
    "temporary_pii_export": 7,
}


def retention_action(dataset_type, created_date, today):
    age_days = (today - created_date).days
    retention_days = POLICIES[dataset_type]

    if age_days > retention_days:
        return f"delete: age={age_days} days, retention={retention_days} days"

    return f"keep: age={age_days} days, retention={retention_days} days"


def main():
    today = date(2026, 7, 2)
    datasets = [
        ("debug_logs", date(2026, 5, 1)),
        ("clickstream_raw", date(2026, 1, 1)),
        ("temporary_pii_export", date(2026, 6, 20)),
    ]

    for dataset_type, created_date in datasets:
        action = retention_action(dataset_type, created_date, today)
        print(f"{dataset_type} created={created_date}: {action}")


if __name__ == "__main__":
    main()
