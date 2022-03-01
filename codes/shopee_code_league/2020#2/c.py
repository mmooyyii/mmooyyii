import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


# https://www.luogu.com.cn/problem/solution/P3402
# 这么难?


class PersistentUnionSet:

    def __init__(self, n):
        import math
        log = math.log(n) * math.log(n) * 2
        self.L = [0] * (log * n)
