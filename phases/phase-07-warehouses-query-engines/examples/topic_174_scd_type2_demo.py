from datetime import date


def close_current_row(row, end_date):
    closed = dict(row)
    closed["effective_end"] = end_date
    closed["is_current"] = False
    return closed


def new_current_row(customer_id, segment, start_date, surrogate_key):
    return {
        "customer_key": surrogate_key,
        "customer_id": customer_id,
        "segment": segment,
        "effective_start": start_date,
        "effective_end": None,
        "is_current": True,
    }


def main():
    current = new_current_row(
        customer_id=10,
        segment="free",
        start_date=date(2026, 1, 1),
        surrogate_key=101,
    )

    changed_segment = "premium"
    change_date = date(2026, 7, 1)

    history = [
        close_current_row(current, change_date),
        new_current_row(10, changed_segment, change_date, 102),
    ]

    print("SCD Type 2 rows:")
    for row in history:
        print(row)

    print("\nOld facts can join to customer_key=101.")
    print("New facts can join to customer_key=102.")


if __name__ == "__main__":
    main()
