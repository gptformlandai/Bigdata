from collections import defaultdict


documents = [
    "hello hadoop hello data",
    "hadoop stores big data",
    "map reduce counts data",
]


def mapper(line):
    for word in line.split():
        yield word, 1


def shuffle(mapped_pairs):
    grouped = defaultdict(list)

    for key, value in mapped_pairs:
        grouped[key].append(value)

    return grouped


def reducer(key, values):
    return key, sum(values)


def main():
    mapped_pairs = []

    for line in documents:
        mapped_pairs.extend(mapper(line))

    grouped = shuffle(mapped_pairs)
    reduced = [reducer(key, grouped[key]) for key in sorted(grouped)]

    print("Mapped pairs:")
    for pair in mapped_pairs:
        print(pair)

    print("\nShuffled groups:")
    for key in sorted(grouped):
        print(key, grouped[key])

    print("\nReduced output:")
    for pair in reduced:
        print(pair)


if __name__ == "__main__":
    main()
