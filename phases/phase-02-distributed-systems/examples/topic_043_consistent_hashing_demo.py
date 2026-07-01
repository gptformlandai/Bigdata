import bisect
import hashlib


class ConsistentHashRing:
    def __init__(self, nodes=None, virtual_nodes=20):
        self.virtual_nodes = virtual_nodes
        self.ring = []
        self.node_by_position = {}

        for node in nodes or []:
            self.add_node(node)

    def _hash(self, value):
        digest = hashlib.md5(value.encode("utf-8")).hexdigest()
        return int(digest, 16)

    def add_node(self, node):
        for replica in range(self.virtual_nodes):
            position = self._hash(f"{node}:{replica}")
            bisect.insort(self.ring, position)
            self.node_by_position[position] = node

    def get_node(self, key):
        if not self.ring:
            raise ValueError("ring has no nodes")

        position = self._hash(key)
        index = bisect.bisect_left(self.ring, position)

        if index == len(self.ring):
            index = 0

        return self.node_by_position[self.ring[index]]


def modulo_assignments(keys, nodes):
    return {
        key: nodes[int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16) % len(nodes)]
        for key in keys
    }


def count_moved(before, after):
    return sum(1 for key in before if before[key] != after[key])


def main():
    keys = [f"user:{number}" for number in range(1, 101)]

    original_nodes = ["node-a", "node-b", "node-c"]
    expanded_nodes = ["node-a", "node-b", "node-c", "node-d"]

    modulo_before = modulo_assignments(keys, original_nodes)
    modulo_after = modulo_assignments(keys, expanded_nodes)

    ring_before = ConsistentHashRing(original_nodes)
    consistent_before = {key: ring_before.get_node(key) for key in keys}

    ring_after = ConsistentHashRing(expanded_nodes)
    consistent_after = {key: ring_after.get_node(key) for key in keys}

    print("Keys:", len(keys))
    print("Modulo hashing moved:", count_moved(modulo_before, modulo_after))
    print("Consistent hashing moved:", count_moved(consistent_before, consistent_after))


if __name__ == "__main__":
    main()
