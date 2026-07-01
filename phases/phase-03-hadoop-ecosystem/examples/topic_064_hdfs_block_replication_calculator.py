import math


def calculate_blocks(file_size_mb, block_size_mb):
    return math.ceil(file_size_mb / block_size_mb)


def main():
    file_size_mb = 1024
    block_size_mb = 128
    replication_factor = 3

    logical_blocks = calculate_blocks(file_size_mb, block_size_mb)
    physical_replicas = logical_blocks * replication_factor
    physical_storage_mb = file_size_mb * replication_factor

    print("File size MB:", file_size_mb)
    print("Block size MB:", block_size_mb)
    print("Logical HDFS blocks:", logical_blocks)
    print("Replication factor:", replication_factor)
    print("Physical block replicas:", physical_replicas)
    print("Approx physical storage MB:", physical_storage_mb)


if __name__ == "__main__":
    main()
