from collections import defaultdict, deque


def topological_order(tasks, dependencies):
    children = defaultdict(list)
    indegree = {task: 0 for task in tasks}

    for upstream, downstream in dependencies:
        children[upstream].append(downstream)
        indegree[downstream] += 1

    ready = deque([task for task in tasks if indegree[task] == 0])
    order = []

    while ready:
        task = ready.popleft()
        order.append(task)

        for child in children[task]:
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)

    if len(order) != len(tasks):
        raise ValueError("Cycle detected. A DAG cannot contain cycles.")

    return order


def main():
    tasks = [
        "extract_orders",
        "extract_customers",
        "validate_orders",
        "build_customer_360",
        "publish_dashboard",
    ]

    dependencies = [
        ("extract_orders", "validate_orders"),
        ("validate_orders", "build_customer_360"),
        ("extract_customers", "build_customer_360"),
        ("build_customer_360", "publish_dashboard"),
    ]

    print("Runnable task order:")
    for position, task in enumerate(topological_order(tasks, dependencies), start=1):
        print(f"{position}. {task}")


if __name__ == "__main__":
    main()
