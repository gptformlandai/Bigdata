def worker_sum(worker_name, amounts):
    subtotal = sum(amounts)
    print(f"{worker_name} scans {amounts} -> subtotal={subtotal}")
    return subtotal


def main():
    partitions = {
        "worker-1": [10, 20, 30],
        "worker-2": [5, 15, 25],
        "worker-3": [100, 50],
    }

    partials = []
    for worker_name, amounts in partitions.items():
        partials.append(worker_sum(worker_name, amounts))

    final_total = sum(partials)
    print(f"\nCoordinator merges partials {partials} -> total={final_total}")


if __name__ == "__main__":
    main()
