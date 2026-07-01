def scan_row_store(rows, needed_columns):
    cells_read = 0
    result = 0

    for row in rows:
        cells_read += len(row)
        result += row["amount"]

    return result, cells_read


def scan_column_store(columns, needed_columns):
    cells_read = 0
    result = 0

    for column_name in needed_columns:
        values = columns[column_name]
        cells_read += len(values)
        if column_name == "amount":
            result = sum(values)

    return result, cells_read


def main():
    rows = [
        {"order_id": 1, "customer": "A", "country": "US", "amount": 50},
        {"order_id": 2, "customer": "B", "country": "IN", "amount": 70},
        {"order_id": 3, "customer": "C", "country": "US", "amount": 30},
    ]

    columns = {
        "order_id": [1, 2, 3],
        "customer": ["A", "B", "C"],
        "country": ["US", "IN", "US"],
        "amount": [50, 70, 30],
    }

    row_total, row_cells = scan_row_store(rows, ["amount"])
    column_total, column_cells = scan_column_store(columns, ["amount"])

    print(f"Row store total: {row_total}, cells read: {row_cells}")
    print(f"Column store total: {column_total}, cells read: {column_cells}")


if __name__ == "__main__":
    main()
