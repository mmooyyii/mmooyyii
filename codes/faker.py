import random
import sys

seed = sys.argv[1]
random.seed(int(seed))


def tree(n):
    nodes = list(range(2, n + 1))
    random.shuffle(nodes)
    edges = []
    t = [1]
    for i in nodes:
        edges.append([random.choice(t), i])
        t.append(i)
    return edges


def graph(a, b):
    pass


n = [0] * 10
for a, b in tree(10):
    n[a - 1] += 1
    n[b - 1] += 1
print(10, 0)
print(*n)
