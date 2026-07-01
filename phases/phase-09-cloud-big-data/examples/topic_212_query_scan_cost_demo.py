def estimate_scan_gb(total_table_gb, selected_column_ratio, partition_ratio):
    return total_table_gb * selected_column_ratio * partition_ratio


def main():
    total_table_gb = 5000

    careless_scan = estimate_scan_gb(
        total_table_gb=total_table_gb,
        selected_column_ratio=1.0,
        partition_ratio=1.0,
    )

    optimized_scan = estimate_scan_gb(
        total_table_gb=total_table_gb,
        selected_column_ratio=0.1,
        partition_ratio=0.02,
    )

    print(f"Careless query scans about {careless_scan:.0f} GB")
    print(f"Optimized query scans about {optimized_scan:.0f} GB")
    print(
        "Optimization came from selecting fewer columns and filtering partitions."
    )


if __name__ == "__main__":
    main()
