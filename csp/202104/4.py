import sys

sys.setrecursionlimit(int(1e9))


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


def make_g(size=10000):
    import random
    from collections import defaultdict
    g = defaultdict(list)
    for i in range(size):
        g[random.randint(0, size - 1)].append(i)
    return g

print(make_g(10))

