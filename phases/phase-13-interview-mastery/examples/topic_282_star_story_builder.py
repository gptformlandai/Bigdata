def build_star_story(situation, task, actions, result, learning):
    print("Situation:")
    print(f"  {situation}")
    print("Task:")
    print(f"  {task}")
    print("Actions:")
    for action in actions:
        print(f"  - {action}")
    print("Result:")
    print(f"  {result}")
    print("Learning:")
    print(f"  {learning}")


def main():
    build_star_story(
        situation="A daily revenue pipeline finished successfully but dashboard numbers were lower than expected.",
        task="Find the issue, protect the report, and restore trusted numbers.",
        actions=[
            "Compared source and target row counts by partition.",
            "Found a new inner join filter removed customers missing a dimension row.",
            "Rolled back the transform and backfilled the affected date.",
            "Added a row-count check and unknown-dimension handling.",
        ],
        result="The dashboard was corrected the same day and the new check caught similar issues before publish.",
        learning="A successful job is not the same as healthy data; publish gates need data checks.",
    )


if __name__ == "__main__":
    main()

