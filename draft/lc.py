from typing import *
from functools import lru_cache


def bf(ls):
    ans = set()
    for i in range(len(ls) - 2):
        for j in range(i + 1, len(ls) - 1):
            for k in range(j + 1, len(ls)):
                v = ls[i] + ls[j] + ls[k]
                if v < 100:
                    ans.add(v)
    for i in range(99, -1, -1):
        if i in ans:
            return i
    raise ValueError


def sv(ls):
    dp = [[0, 0, 0] for _ in range(100)]
    for i in ls:
        tmp = [[0, 0, 0] for _ in range(100)]
        for j, n in enumerate(dp):
            if 0 <= i + j < 100:
                tmp[i + j] = [0, n[0], n[1]]
        if 0 <= i < 100:
            tmp[i][0] = 1
        for i, n in enumerate(tmp):
            dp[i] = [max(dp[i][0], n[0]), max(dp[i][1], n[1]), max(dp[i][2], n[2])]

    for i in range(99, -1, -1):
        if dp[i][-1] == 1:
            return i
    raise ValueError


import random

ls = [random.randint(1, 10) for _ in range(20)]
print(bf(ls))
print(sv(ls))
