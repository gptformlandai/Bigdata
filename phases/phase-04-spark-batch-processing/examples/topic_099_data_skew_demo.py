from collections import Counter


events = (
    ["US"] * 80
    + ["IN"] * 8
    + ["CA"] * 5
    + ["GB"] * 4
    + ["DE"] * 3
)


def main():
    counts = Counter(events)
    total = len(events)

    print("Total events:", total)
    print("Counts by key:")

    for key, count in counts.most_common():
        percent = round((count / total) * 100, 2)
        print(f"{key}: {count} events ({percent}%)")

    hottest_key, hottest_count = counts.most_common(1)[0]
    print("\nHot key:", hottest_key)
    print("Why it matters: one Spark reducer task may get most rows for this key.")

    salted_keys = [f"{hottest_key}#{salt}" for salt in range(4)]
    print("Possible salted keys:", salted_keys)


if __name__ == "__main__":
    main()
