def apply_change(table, event):
    key = event["key"]
    operation = event["op"]

    if operation in ("insert", "update"):
        table[key] = event["after"]
    elif operation == "delete":
        table.pop(key, None)
    else:
        raise ValueError(f"Unknown operation: {operation}")


def main():
    current_orders = {}

    cdc_events = [
        {"op": "insert", "key": 1, "after": {"order_id": 1, "status": "created", "amount": 50}},
        {"op": "update", "key": 1, "after": {"order_id": 1, "status": "paid", "amount": 50}},
        {"op": "insert", "key": 2, "after": {"order_id": 2, "status": "created", "amount": 90}},
        {"op": "delete", "key": 1, "after": None},
    ]

    for event in cdc_events:
        apply_change(current_orders, event)
        print(f"After {event['op']} key={event['key']}: {current_orders}")


if __name__ == "__main__":
    main()

