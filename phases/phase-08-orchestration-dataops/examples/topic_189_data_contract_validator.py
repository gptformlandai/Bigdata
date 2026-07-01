CONTRACT = {
    "required_fields": ["order_id", "amount_cents", "currency"],
    "accepted_currency": {"USD", "INR", "EUR"},
}


def validate_order_event(event):
    errors = []

    for field in CONTRACT["required_fields"]:
        if field not in event or event[field] is None:
            errors.append(f"{field} is required")

    amount = event.get("amount_cents")
    if amount is not None and amount < 0:
        errors.append("amount_cents must be >= 0")

    currency = event.get("currency")
    if currency is not None and currency not in CONTRACT["accepted_currency"]:
        errors.append(f"currency {currency} is not accepted")

    return errors


def main():
    events = [
        {"order_id": "o-1", "amount_cents": 1200, "currency": "USD"},
        {"order_id": "o-2", "amount_cents": -10, "currency": "USD"},
        {"order_id": None, "amount_cents": 700, "currency": "BTC"},
    ]

    for event in events:
        errors = validate_order_event(event)
        status = "valid" if not errors else f"invalid: {errors}"
        print(f"{event} -> {status}")


if __name__ == "__main__":
    main()
