def tree(n):
    nodes = list(range(2, n + 1))
    import random
    random.shuffle(nodes)
    edges = []
    t = [1]
    for i in nodes:
        edges.append([random.choice(t), i])
        t.append(i)
    for a, b in edges:
        print(a, b)


def graph(a, b):
    pass
