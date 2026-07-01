def route_alert(dataset, issue, criticality):
    if criticality == "critical" and issue in {"sla_missed", "quality_failed"}:
        return "P1 page data-oncall"

    if criticality == "high":
        return "P2 notify owning team channel"

    if issue == "cost_spike":
        return "P3 notify platform channel"

    return "P4 create ticket"


def main():
    alerts = [
        ("daily_revenue", "sla_missed", "critical"),
        ("orders_silver", "quality_failed", "high"),
        ("experiment_table", "freshness_delay", "low"),
        ("warehouse_queries", "cost_spike", "medium"),
    ]

    for dataset, issue, criticality in alerts:
        route = route_alert(dataset, issue, criticality)
        print(f"{dataset}: issue={issue}, criticality={criticality} -> {route}")


if __name__ == "__main__":
    main()
