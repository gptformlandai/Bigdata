def build_time_plan(total_minutes):
    sections = [
        ("clarify requirements", 0.12),
        ("estimate scale and define events", 0.12),
        ("draw high-level architecture", 0.22),
        ("deep dive critical components", 0.27),
        ("failures, scaling, monitoring", 0.17),
        ("trade-offs and final summary", 0.10),
    ]

    plan = []
    elapsed = 0

    for name, fraction in sections:
        minutes = round(total_minutes * fraction)
        start = elapsed
        end = elapsed + minutes
        plan.append((start, end, name))
        elapsed = end

    if plan[-1][1] != total_minutes:
        start, _, name = plan[-1]
        plan[-1] = (start, total_minutes, name)

    return plan


def main():
    for start, end, name in build_time_plan(45):
        print(f"{start:02d}-{end:02d} min: {name}")


if __name__ == "__main__":
    main()

