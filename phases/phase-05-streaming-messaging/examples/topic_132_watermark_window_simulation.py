from collections import defaultdict


events = [
    {"id": "e1", "event_minute": 1, "arrival_minute": 1},
    {"id": "e2", "event_minute": 2, "arrival_minute": 2},
    {"id": "e3", "event_minute": 4, "arrival_minute": 4},
    {"id": "e4", "event_minute": 3, "arrival_minute": 8},
    {"id": "e5", "event_minute": 7, "arrival_minute": 7},
]


def window_start(event_minute, window_size):
    return (event_minute // window_size) * window_size


def main():
    allowed_lateness = 2
    window_size = 5
    max_event_time_seen = -1
    windows = defaultdict(list)
    late_events = []

    for event in sorted(events, key=lambda item: item["arrival_minute"]):
        max_event_time_seen = max(max_event_time_seen, event["event_minute"])
        watermark = max_event_time_seen - allowed_lateness

        if event["event_minute"] < watermark:
            late_events.append(event["id"])
            status = "late"
        else:
            start = window_start(event["event_minute"], window_size)
            windows[start].append(event["id"])
            status = f"accepted into window {start}-{start + window_size}"

        print(
            f"arrival={event['arrival_minute']}, event={event['id']}, "
            f"event_time={event['event_minute']}, watermark={watermark}, {status}"
        )

    print("\nWindows:")
    for start in sorted(windows):
        print(f"{start}-{start + window_size}: {windows[start]}")

    print("Late events:", late_events)


if __name__ == "__main__":
    main()
