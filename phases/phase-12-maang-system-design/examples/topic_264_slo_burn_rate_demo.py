def error_budget_burn_rate(total_requests, failed_requests, slo_success_rate):
    allowed_error_rate = 1 - slo_success_rate
    actual_error_rate = failed_requests / total_requests
    return actual_error_rate / allowed_error_rate


def classify_alert(burn_rate):
    if burn_rate >= 14:
        return "page immediately"
    if burn_rate >= 6:
        return "urgent ticket"
    if burn_rate >= 2:
        return "watch closely"
    return "healthy"


def main():
    windows = [
        {"name": "last_5m", "total": 100_000, "failed": 300},
        {"name": "last_1h", "total": 1_200_000, "failed": 1_500},
        {"name": "last_6h", "total": 7_200_000, "failed": 3_000},
    ]

    slo = 0.999

    for window in windows:
        burn = error_budget_burn_rate(window["total"], window["failed"], slo)
        print(f"{window['name']}: burn_rate={burn:.2f}, action={classify_alert(burn)}")


if __name__ == "__main__":
    main()

