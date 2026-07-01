def process_at_most_once(events):
    processed = []

    for event in events:
        committed = True
        failed = event == "e2"

        if committed and failed:
            continue

        processed.append(event)

    return processed


def process_at_least_once(events):
    processed = []

    for event in events:
        processed.append(event)

        if event == "e2":
            processed.append(event)

    return processed


def process_idempotently(events):
    processed = []
    seen = set()

    for event in process_at_least_once(events):
        if event in seen:
            continue

        seen.add(event)
        processed.append(event)

    return processed


def main():
    events = ["e1", "e2", "e3"]

    print("Input:", events)
    print("At-most-once result:", process_at_most_once(events))
    print("At-least-once result:", process_at_least_once(events))
    print("Idempotent final result:", process_idempotently(events))


if __name__ == "__main__":
    main()
