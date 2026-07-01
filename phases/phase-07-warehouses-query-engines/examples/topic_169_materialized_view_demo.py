def build_daily_sales_view(orders):
    view = {}
    for order in orders:
        key = (order["date"], order["region"])
        view[key] = view.get(key, 0) + order["amount"]
    return view


def main():
    orders = [
        {"date": "2026-07-01", "region": "east", "amount": 100},
        {"date": "2026-07-01", "region": "east", "amount": 50},
        {"date": "2026-07-01", "region": "west", "amount": 80},
        {"date": "2026-07-02", "region": "east", "amount": 40},
    ]

    materialized_view = build_daily_sales_view(orders)

    print("Materialized daily_sales view:")
    for (date, region), revenue in sorted(materialized_view.items()):
        print(f"{date} {region}: revenue={revenue}")

    print("\nDashboard can read this small summary instead of raw orders.")


if __name__ == "__main__":
    main()
