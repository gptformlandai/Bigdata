def copy_on_write_update(base_file_mb, updates):
    rewritten_mb = base_file_mb
    read_merge_files = 1
    return rewritten_mb, read_merge_files


def merge_on_read_update(base_file_mb, updates, update_record_kb):
    written_mb = (updates * update_record_kb) / 1024
    read_merge_files = 2
    return round(written_mb, 2), read_merge_files


def main():
    base_file_mb = 256
    updates = 100
    update_record_kb = 2

    cow_write_mb, cow_read_files = copy_on_write_update(base_file_mb, updates)
    mor_write_mb, mor_read_files = merge_on_read_update(
        base_file_mb,
        updates,
        update_record_kb,
    )

    print("Updating 100 records inside a 256 MB data file\n")

    print("Copy-on-write")
    print(f"write cost: rewrite about {cow_write_mb} MB")
    print(f"read path: read {cow_read_files} latest base file\n")

    print("Merge-on-read")
    print(f"write cost: write about {mor_write_mb} MB of change records")
    print(f"read path: merge {mor_read_files} files before compaction")


if __name__ == "__main__":
    main()
