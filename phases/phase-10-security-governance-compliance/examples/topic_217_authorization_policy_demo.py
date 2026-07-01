POLICIES = {
    "finance_reader": {
        ("SELECT", "gold.revenue"),
        ("SELECT", "gold.invoice_summary"),
    },
    "product_reader": {
        ("SELECT", "gold.product_metrics"),
    },
    "etl_writer": {
        ("READ", "bronze.orders"),
        ("WRITE", "silver.orders"),
    },
}


USERS = {
    "alice": {"finance_reader"},
    "bob": {"product_reader"},
    "orders_job": {"etl_writer"},
}


def is_allowed(principal, action, resource):
    roles = USERS.get(principal, set())
    for role in roles:
        if (action, resource) in POLICIES.get(role, set()):
            return True
    return False


def main():
    checks = [
        ("alice", "SELECT", "gold.revenue"),
        ("bob", "SELECT", "gold.revenue"),
        ("orders_job", "WRITE", "silver.orders"),
        ("orders_job", "DELETE", "silver.orders"),
    ]

    for principal, action, resource in checks:
        result = "ALLOW" if is_allowed(principal, action, resource) else "DENY"
        print(f"{principal} {action} {resource}: {result}")


if __name__ == "__main__":
    main()
