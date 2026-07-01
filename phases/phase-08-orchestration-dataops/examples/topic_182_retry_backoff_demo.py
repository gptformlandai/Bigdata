def run_with_retries(operation, max_attempts, base_delay_seconds):
    for attempt in range(1, max_attempts + 1):
        try:
            result = operation(attempt)
            print(f"attempt {attempt}: success -> {result}")
            return result
        except RuntimeError as error:
            print(f"attempt {attempt}: failed -> {error}")

            if attempt == max_attempts:
                print("no retries left")
                raise

            delay = base_delay_seconds * (2 ** (attempt - 1))
            print(f"wait {delay} seconds before retry")


def flaky_warehouse_load(attempt):
    if attempt < 3:
        raise RuntimeError("temporary warehouse timeout")
    return "loaded orders partition"


def main():
    run_with_retries(
        operation=flaky_warehouse_load,
        max_attempts=4,
        base_delay_seconds=30,
    )


if __name__ == "__main__":
    main()
