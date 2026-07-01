from collections import Counter


raw_events = [
    {"event_id": "e1", "user_id": "u1", "event_type": "view"},
    {"event_id": "e2", "user_id": "u1", "event_type": "click"},
    {"event_id": "e3", "user_id": "u2", "event_type": "purchase"},
    {"event_id": "e4", "event_type": "click"},
    {"user_id": "u3", "event_type": "view"},
    {"event_id": "e6", "user_id": "u4", "event_type": "view"},
]


REQUIRED_FIELDS = {"event_id", "user_id", "event_type"}


def is_valid(event):
    return REQUIRED_FIELDS.issubset(event.keys())


def main():
    valid_events = []
    bad_events = []

    for event in raw_events:
        if is_valid(event):
            valid_events.append(event)
        else:
            bad_events.append(event)

    counts = Counter(event["event_type"] for event in valid_events)

    print("Valid events:", len(valid_events))
    print("Bad events:", len(bad_events))
    print("Event counts:", dict(counts))
    print("Bad records:", bad_events)


if __name__ == "__main__":
    main()
