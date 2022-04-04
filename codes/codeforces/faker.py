import random
import sys

if len(sys.argv) >= 2:
    seed = sys.argv[1]
    random.seed(int(seed))


def tree(n):
    nodes = list(range(2, n + 1))
    import random
    random.shuffle(nodes)
    edges = []
    t = [1]
    for i in nodes:
        edges.append([random.choice(t), i])
        t.append(i)
    return edges


xx = 100000
n = [0] * xx
ee = tree(xx)
for a, b in ee:
    n[a - 1] += 1
    n[b - 1] += 1
c = random.randint(0, xx - 2)
print(xx, c)
print(*n)
for i in random.sample(ee, c):
    print(*i)
