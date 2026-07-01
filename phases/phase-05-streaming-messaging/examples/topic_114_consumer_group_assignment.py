def assign_partitions(partitions, consumers):
    assignment = {consumer: [] for consumer in consumers}

    for index, partition in enumerate(partitions):
        consumer = consumers[index % len(consumers)]
        assignment[consumer].append(partition)

    return assignment


def main():
    partitions = [f"orders-{number}" for number in range(6)]

    for consumers in [
        ["consumer-a"],
        ["consumer-a", "consumer-b"],
        ["consumer-a", "consumer-b", "consumer-c"],
        ["consumer-a", "consumer-b", "consumer-c", "consumer-d", "consumer-e", "consumer-f", "consumer-g"],
    ]:
        print("\nConsumers:", consumers)
        assignment = assign_partitions(partitions, consumers)

        for consumer, assigned in assignment.items():
            print(f"{consumer}: {assigned}")


if __name__ == "__main__":
    main()
