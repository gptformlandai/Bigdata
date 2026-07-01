def merge_by_key(existing_rows, updates, key):
    merged = {row[key]: dict(row) for row in existing_rows}

    for update in updates:
        merged[update[key]] = dict(update)

    return [merged[row_key] for row_key in sorted(merged)]


def main():
    customers = [
        {"customer_id": 1, "city": "Austin", "version": 1},
        {"customer_id": 2, "city": "Seattle", "version": 1},
    ]

    updates = [
        {"customer_id": 1, "city": "Dallas", "version": 2},
        {"customer_id": 3, "city": "Boston", "version": 1},
    ]

    print("Before:")
    for row in customers:
        print(row)

    print("\nUpdates:")
    for row in updates:
        print(row)

    print("\nAfter upsert:")
    for row in merge_by_key(customers, updates, "customer_id"):
        print(row)


if __name__ == "__main__":
    main()
