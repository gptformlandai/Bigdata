class FakeBroker:
    def __init__(self):
        self.published_event_ids = set()

    def publish(self, event):
        event_id = event["event_id"]
        if event_id in self.published_event_ids:
            print(f"Skip duplicate publish: {event_id}")
            return

        self.published_event_ids.add(event_id)
        print(f"Published {event['event_type']} for aggregate {event['aggregate_id']}")


def create_order(database, order_id, amount):
    database["orders"][order_id] = {"order_id": order_id, "amount": amount, "status": "created"}
    database["outbox"].append(
        {
            "event_id": f"order-{order_id}-created",
            "aggregate_id": order_id,
            "event_type": "OrderCreated",
            "payload": {"order_id": order_id, "amount": amount},
            "published": False,
        }
    )


def relay_outbox(database, broker):
    for event in database["outbox"]:
        if not event["published"]:
            broker.publish(event)
            event["published"] = True


def main():
    database = {"orders": {}, "outbox": []}
    broker = FakeBroker()

    create_order(database, order_id=101, amount=75)
    create_order(database, order_id=102, amount=120)

    print("Business table:", database["orders"])
    print("\nRelay run 1:")
    relay_outbox(database, broker)

    database["outbox"][0]["published"] = False
    print("\nRelay run 2 after retry/bug:")
    relay_outbox(database, broker)


if __name__ == "__main__":
    main()

