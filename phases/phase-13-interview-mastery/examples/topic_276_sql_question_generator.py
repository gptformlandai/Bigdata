QUESTIONS = [
    "Find the latest event per user using row_number.",
    "Calculate 7-day rolling revenue by product.",
    "Find the top 3 products per category by sales.",
    "Deduplicate events by event_id keeping the newest event_time.",
    "Join orders to a Type 2 customer dimension as of order_date.",
    "Calculate view -> cart -> purchase funnel conversion.",
    "Find users active for 3 consecutive days.",
    "Identify customers who purchased product A but never product B.",
]


def main():
    print("SQL practice prompts:")
    for index, question in enumerate(QUESTIONS, start=1):
        print(f"{index}. {question}")


if __name__ == "__main__":
    main()

