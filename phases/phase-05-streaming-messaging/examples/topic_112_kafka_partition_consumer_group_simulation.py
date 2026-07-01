import hashlib


def choose_partition(key, partition_count):
    digest = hashlib.md5(key.encode("utf-8")).hexdigest()
    return int(digest, 16) % partition_count


def assign_partitions(partition_count, consumers):
    assignments = {consumer: [] for consumer in consumers}

    for partition in range(partition_count):
        consumer = consumers[partition % len(consumers)]
        assignments[consumer].append(partition)

    return assignments


def main():
    partition_count = 4
    events = [
        ("user-1", "click"),
        ("user-2", "view"),
        ("user-1", "purchase"),
        ("user-3", "click"),
        ("user-2", "purchase"),
    ]

    print("Event partitioning:")
    for key, event_type in events:
        partition = choose_partition(key, partition_count)
        print(f"key={key}, event={event_type}, partition={partition}")

    print("\nConsumer group assignment:")
    assignments = assign_partitions(partition_count, ["consumer-a", "consumer-b"])

    for consumer, partitions in assignments.items():
        print(f"{consumer}: partitions={partitions}")


if __name__ == "__main__":
    main()
