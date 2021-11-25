from typing import *
import random


def pop_loop(edge):
    node = max(edge.keys())
    loop = [node]
    while True:
        nxt = edge[node][-1]
        if nxt == loop[0]:
            edge[node].remove(loop[0])
            if not edge[node]:
                edge.pop(node)
            break
        edge[node].pop()
        if not edge[node]:
            edge.pop(node)
        loop.append(nxt)
        node = nxt

    return len(loop)


def bf(ls):
    from itertools import permutations
    from collections import defaultdict
    c = list(Counter(ls).items())
    ans = 1e9
    for psb in permutations(c):
        target = []
        for k, v in psb:
            target.extend([k] * v)
        edge = defaultdict(list)
        for i in range(len(ls)):
            if target[i] != ls[i]:
                edge[target[i]].append(ls[i])
        tmp = 0
        while edge:
            tmp += pop_loop(edge) - 1
        ans = min(ans, tmp)
        if ans == tmp:
            print(psb, tmp)
    return ans


a = []
for i in range(1, 6):
    a.extend([i] * random.randint(1, 10))
random.shuffle(a)
print(len(a), a)
print(bf(a))


def dp(idx, used):
    pass
