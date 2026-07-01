from collections import defaultdict


def minute_bucket(timestamp):
    return timestamp[:16]


def rollup_counts(events):
    counts = defaultdict(int)

    for event in events:
        key = (minute_bucket(event["timestamp"]), event["service"], event["status"])
        counts[key] += 1

    return counts


def main():
    request_events = [
        {"timestamp": "2026-07-02 10:00:01", "service": "checkout", "status": "200"},
        {"timestamp": "2026-07-02 10:00:10", "service": "checkout", "status": "200"},
        {"timestamp": "2026-07-02 10:00:13", "service": "checkout", "status": "500"},
        {"timestamp": "2026-07-02 10:01:02", "service": "checkout", "status": "200"},
        {"timestamp": "2026-07-02 10:01:04", "service": "search", "status": "200"},
    ]

    counts = rollup_counts(request_events)

    for (bucket, service, status), count in sorted(counts.items()):
        print(f"requests_total minute={bucket} service={service} status={status} count={count}")


if __name__ == "__main__":
    main()

