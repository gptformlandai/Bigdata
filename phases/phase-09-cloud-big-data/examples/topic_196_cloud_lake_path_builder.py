def build_lake_path(cloud, zone, dataset, date):
    if cloud == "aws":
        return f"s3://company-lake/{zone}/{dataset}/dt={date}/"
    if cloud == "gcp":
        return f"gs://company-lake/{zone}/{dataset}/dt={date}/"
    if cloud == "azure":
        return (
            "abfss://lake@companylake.dfs.core.windows.net/"
            f"{zone}/{dataset}/dt={date}/"
        )

    raise ValueError(f"Unknown cloud: {cloud}")


def main():
    for cloud in ["aws", "gcp", "azure"]:
        path = build_lake_path(
            cloud=cloud,
            zone="silver",
            dataset="orders",
            date="2026-07-01",
        )
        print(f"{cloud}: {path}")


if __name__ == "__main__":
    main()
