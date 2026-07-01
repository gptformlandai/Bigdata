from collections import defaultdict


partitions = [
    [("c1", 10), ("c2", 7), ("c1", 3)],
    [("c3", 4), ("c2", 5), ("c1", 8)],
    [("c3", 6), ("c4", 1)],
]


def shuffle_by_key(input_partitions):
    grouped = defaultdict(list)

    for partition_id, rows in enumerate(input_partitions):
        for key, value in rows:
            print(f"map partition={partition_id}, emit {key} -> {value}")
            grouped[key].append(value)

    return grouped


def reduce_groups(grouped):
    return {
        key: sum(values)
        for key, values in sorted(grouped.items())
    }


def main():
    grouped = shuffle_by_key(partitions)

    print("\nAfter shuffle, values are grouped by key:")
    for key in sorted(grouped):
        print(key, grouped[key])

    print("\nReduced output:")
    print(reduce_groups(grouped))


if __name__ == "__main__":
    main()
