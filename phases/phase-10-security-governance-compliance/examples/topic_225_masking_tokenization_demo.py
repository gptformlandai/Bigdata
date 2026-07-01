import hashlib


def mask_email(email):
    local, domain = email.split("@", 1)
    return f"{local[0]}***@{domain}"


def tokenize(value, secret):
    digest = hashlib.sha256(f"{secret}:{value}".encode("utf-8")).hexdigest()
    return f"tok_{digest[:10]}"


def main():
    customer = {
        "customer_id": 123,
        "email": "alice@example.com",
        "phone": "555-123-9876",
    }

    print("Raw:")
    print(customer)

    print("\nMasked for support:")
    print(
        {
            "customer_id": customer["customer_id"],
            "email": mask_email(customer["email"]),
            "phone": "XXX-XXX-" + customer["phone"][-4:],
        }
    )

    print("\nTokenized for analytics joins:")
    print(
        {
            "customer_token": tokenize(customer["email"], secret="demo-secret"),
            "phone_last4": customer["phone"][-4:],
        }
    )


if __name__ == "__main__":
    main()
