from collections import defaultdict
from datetime import datetime, timedelta


events = [
    {"id": "e1", "event_time": "10:00", "arrival_time": "10:00", "amount": 10},
    {"id": "e2", "event_time": "10:01", "arrival_time": "10:01", "amount": 20},
    {"id": "e3", "event_time": "10:04", "arrival_time": "10:04", "amount": 30},
    {"id": "e4", "event_time": "10:01", "arrival_time": "10:07", "amount": 40},
    {"id": "e5", "event_time": "10:06", "arrival_time": "10:08", "amount": 50},
]


def parse_time(value):
    return datetime.strptime(value, "%H:%M")


def window_start(event_time, window_minutes=5):
    minute = (event_time.minute // window_minutes) * window_minutes
    return event_time.replace(minute=minute)


def main():
    allowed_lateness = timedelta(minutes=2)
    max_event_time = None
    windows = defaultdict(int)
    late_events = []

    for event in sorted(events, key=lambda item: parse_time(item["arrival_time"])):
        event_time = parse_time(event["event_time"])

        if max_event_time is None or event_time > max_event_time:
            max_event_time = event_time

        watermark = max_event_time - allowed_lateness

        if event_time < watermark:
            late_events.append(event["id"])
            status = "late"
        else:
            start = window_start(event_time)
            windows[start.strftime("%H:%M")] += event["amount"]
            status = "accepted"

        print(
            f"event={event['id']} event_time={event['event_time']} "
            f"arrival={event['arrival_time']} watermark={watermark.strftime('%H:%M')} status={status}"
        )

    print("\nWindow totals:", dict(windows))
    print("Late events:", late_events)


if __name__ == "__main__":
    main()
