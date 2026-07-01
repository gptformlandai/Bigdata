import hashlib


def choose_partition(partition_key, partition_count):
    digest = hashlib.md5(partition_key.encode("utf-8")).hexdigest()
    return int(digest, 16) % partition_count


def main():
    events = [
        {"user_id": "u-1", "event": "click"},
        {"user_id": "u-2", "event": "view"},
        {"user_id": "u-1", "event": "purchase"},
        {"user_id": "u-3", "event": "click"},
        {"user_id": "u-2", "event": "logout"},
    ]

    partition_count = 4

    for event in events:
        partition = choose_partition(event["user_id"], partition_count)
        print(
            f"user={event['user_id']} event={event['event']} "
            f"-> partition={partition}"
        )

    print("\nSame user_id goes to the same partition, preserving per-user order.")


if __name__ == "__main__":
    main()
