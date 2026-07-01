ROWS = [
    {"region": "US", "customer": "A", "email": "a@example.com", "revenue": 100},
    {"region": "EU", "customer": "B", "email": "b@example.com", "revenue": 80},
    {"region": "US", "customer": "C", "email": "c@example.com", "revenue": 50},
]


USERS = {
    "us_manager": {"regions": {"US"}, "can_see_email": False},
    "privacy_admin": {"regions": {"US", "EU"}, "can_see_email": True},
}


def query_rows(user_name):
    user = USERS[user_name]
    result = []

    for row in ROWS:
        if row["region"] not in user["regions"]:
            continue

        visible = dict(row)
        if not user["can_see_email"]:
            visible["email"] = "***masked***"
        result.append(visible)

    return result


def main():
    for user_name in USERS:
        print(f"\n{user_name} sees:")
        for row in query_rows(user_name):
            print(row)


if __name__ == "__main__":
    main()
