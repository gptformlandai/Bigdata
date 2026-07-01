import random


def retry_delays(max_attempts, base_seconds=1.0, cap_seconds=30.0, seed=7):
    random.seed(seed)
    delays = []

    for attempt in range(max_attempts):
        exponential_delay = min(cap_seconds, base_seconds * (2 ** attempt))
        jitter = random.uniform(0, exponential_delay * 0.2)
        delays.append(round(min(cap_seconds, exponential_delay + jitter), 2))

    return delays


def main():
    for attempt, delay in enumerate(retry_delays(max_attempts=6), start=1):
        print(f"attempt={attempt}, wait_seconds={delay}")


if __name__ == "__main__":
    main()
