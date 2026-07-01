from datetime import datetime


def month_partition(order_ts):
    return order_ts.strftime("%Y-%m")


def day_partition(order_ts):
    return order_ts.strftime("%Y-%m-%d")


def plan_file(order_id, order_ts, partition_spec):
    if partition_spec == "month":
        partition = month_partition(order_ts)
    elif partition_spec == "day":
        partition = day_partition(order_ts)
    else:
        raise ValueError(f"Unknown spec: {partition_spec}")

    return {
        "file": f"orders_{order_id}.parquet",
        "spec": partition_spec,
        "partition": partition,
    }


def main():
    files = [
        plan_file(1, datetime(2026, 6, 20), "month"),
        plan_file(2, datetime(2026, 6, 21), "month"),
        plan_file(3, datetime(2026, 7, 1), "day"),
        plan_file(4, datetime(2026, 7, 2), "day"),
    ]

    print("One table can contain files written with old and new partition specs:\n")
    for file_info in files:
        print(
            f"{file_info['file']}: "
            f"spec={file_info['spec']}, partition={file_info['partition']}"
        )

    print("\nMetadata tells the planner which spec belongs to each file.")


if __name__ == "__main__":
    main()
