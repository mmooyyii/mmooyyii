import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


from functools import lru_cache

import random
import time
import heapq

data = [random.randint(1, 1000000) for _ in range(int(int(1e6)))]


def use_heap():
    h = []
    for i in data:
        if len(h) < 10:
            heapq.heappush(h, -i)
        else:
            heapq.heappushpop(h, -i)
    return -h[0]


import bisect


def use_max():
    h = []
    for i in data:
        if len(h) < 10:
            h.append(i)
            if len(h) == 10:
                h.sort()
        else:
            if h[-1] > i:
                h.pop()
                bisect.insort(h, i)
    return max(h)


s = time.time()
print("ans:", use_heap())
print(time.time() - s)

s = time.time()
print("ans:", use_max())
print(time.time() - s)
