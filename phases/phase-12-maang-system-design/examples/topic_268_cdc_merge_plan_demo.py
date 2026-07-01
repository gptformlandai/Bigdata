def build_merge_plan(cdc_events):
    latest_by_key = {}

    for event in cdc_events:
        key = event["key"]
        if key not in latest_by_key or event["source_offset"] > latest_by_key[key]["source_offset"]:
            latest_by_key[key] = event

    plan = []
    for key, event in sorted(latest_by_key.items()):
        if event["op"] == "delete":
            plan.append({"action": "delete", "key": key})
        elif event["op"] in ("insert", "update"):
            plan.append({"action": "upsert", "key": key, "row": event["after"]})
        else:
            plan.append({"action": "quarantine", "key": key, "reason": "unknown operation"})

    return plan


def main():
    events = [
        {"key": 1, "op": "insert", "after": {"order_id": 1, "status": "created"}, "source_offset": 10},
        {"key": 1, "op": "update", "after": {"order_id": 1, "status": "paid"}, "source_offset": 11},
        {"key": 2, "op": "insert", "after": {"order_id": 2, "status": "created"}, "source_offset": 12},
        {"key": 2, "op": "delete", "after": None, "source_offset": 13},
        {"key": 1, "op": "update", "after": {"order_id": 1, "status": "shipped"}, "source_offset": 9},
    ]

    for action in build_merge_plan(events):
        print(action)


if __name__ == "__main__":
    main()

