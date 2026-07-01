from datetime import datetime


def parse_time(value):
    return datetime.strptime(value, "%Y-%m-%d %H:%M")


def point_in_time_lookup(feature_rows, entity_id, as_of_time):
    candidates = [
        row
        for row in feature_rows
        if row["user_id"] == entity_id and parse_time(row["feature_time"]) <= as_of_time
    ]

    if not candidates:
        return None

    return max(candidates, key=lambda row: parse_time(row["feature_time"]))


def main():
    purchase_features = [
        {"user_id": "u1", "feature_time": "2026-07-01 09:00", "purchases_7d": 2},
        {"user_id": "u1", "feature_time": "2026-07-01 12:00", "purchases_7d": 3},
        {"user_id": "u1", "feature_time": "2026-07-01 18:00", "purchases_7d": 5},
    ]

    training_examples = [
        {"user_id": "u1", "label_time": "2026-07-01 10:00", "label": "not_fraud"},
        {"user_id": "u1", "label_time": "2026-07-01 20:00", "label": "fraud"},
    ]

    for example in training_examples:
        as_of_time = parse_time(example["label_time"])
        feature = point_in_time_lookup(purchase_features, example["user_id"], as_of_time)
        print(f"Label at {example['label_time']} uses feature: {feature}")


if __name__ == "__main__":
    main()

