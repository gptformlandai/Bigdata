class TinyLazyFrame:
    def __init__(self, rows, plan=None):
        self.rows = rows
        self.plan = plan or []

    def filter(self, predicate):
        return TinyLazyFrame(self.rows, self.plan + [("filter", predicate)])

    def map(self, mapper):
        return TinyLazyFrame(self.rows, self.plan + [("map", mapper)])

    def collect(self):
        print("Action triggered. Running plan now.")
        result = self.rows

        for operation, function in self.plan:
            if operation == "filter":
                result = [row for row in result if function(row)]
            elif operation == "map":
                result = [function(row) for row in result]

        return result


def main():
    frame = TinyLazyFrame([1, 2, 3, 4, 5])

    planned = (
        frame
        .filter(lambda value: value % 2 == 0)
        .map(lambda value: value * 10)
    )

    print("Transformations were defined, but not executed yet.")
    print("Plan length:", len(planned.plan))
    print("Result:", planned.collect())


if __name__ == "__main__":
    main()
