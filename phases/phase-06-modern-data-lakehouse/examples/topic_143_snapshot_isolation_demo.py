class LakehouseTable:
    def __init__(self):
        self.snapshots = {
            1: ["orders_001.parquet", "orders_002.parquet"],
        }
        self.current_snapshot_id = 1

    def start_query(self):
        return self.current_snapshot_id

    def read_files(self, snapshot_id):
        return list(self.snapshots[snapshot_id])

    def commit_new_snapshot(self, added_files):
        old_files = self.snapshots[self.current_snapshot_id]
        new_snapshot_id = self.current_snapshot_id + 1
        self.snapshots[new_snapshot_id] = old_files + added_files
        self.current_snapshot_id = new_snapshot_id
        return new_snapshot_id


def main():
    table = LakehouseTable()

    query_a_snapshot = table.start_query()
    print(f"Query A starts on snapshot {query_a_snapshot}")
    print("Query A files:", table.read_files(query_a_snapshot))

    committed = table.commit_new_snapshot(["orders_003.parquet"])
    print(f"\nWriter commits snapshot {committed}")

    print("\nQuery A still sees:", table.read_files(query_a_snapshot))

    query_b_snapshot = table.start_query()
    print(f"Query B starts on snapshot {query_b_snapshot}")
    print("Query B sees:", table.read_files(query_b_snapshot))


if __name__ == "__main__":
    main()
