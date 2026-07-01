def estimate_volume(daily_users, events_per_user_per_day, avg_event_size_bytes, compression_ratio):
    events_per_day = daily_users * events_per_user_per_day
    raw_tb_per_day = events_per_day * avg_event_size_bytes / (1024 ** 4)
    compressed_tb_per_day = raw_tb_per_day / compression_ratio
    return events_per_day, raw_tb_per_day, compressed_tb_per_day


def recommend_partitions(events_per_day, target_events_per_partition_per_day):
    partitions = events_per_day // target_events_per_partition_per_day
    if events_per_day % target_events_per_partition_per_day:
        partitions += 1
    return max(1, partitions)


def main():
    scenarios = [
        {
            "name": "youtube_playback",
            "daily_users": 500_000_000,
            "events_per_user": 100,
            "event_size": 1_000,
            "compression_ratio": 4,
        },
        {
            "name": "amazon_clickstream",
            "daily_users": 300_000_000,
            "events_per_user": 80,
            "event_size": 1_000,
            "compression_ratio": 4,
        },
    ]

    for scenario in scenarios:
        events, raw_tb, compressed_tb = estimate_volume(
            scenario["daily_users"],
            scenario["events_per_user"],
            scenario["event_size"],
            scenario["compression_ratio"],
        )
        partitions = recommend_partitions(events, target_events_per_partition_per_day=100_000_000)

        print(f"{scenario['name']}:")
        print(f"  events/day: {events:,}")
        print(f"  raw TB/day: {raw_tb:.2f}")
        print(f"  compressed TB/day: {compressed_tb:.2f}")
        print(f"  rough daily partitions/shards: {partitions}")


if __name__ == "__main__":
    main()

