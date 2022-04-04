import random
import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_ls():
    return list(input().split())


def cin_int():
    return int(input())


class UnionFind:
    def __init__(self, n):
        from collections import defaultdict
        self.uf = defaultdict(lambda: -1)
        self.set = set()
        self.count_ = n

    def find(self, x):
        r = x
        while self.uf[x] >= 0:
            x = self.uf[x]
        while r != x:
            self.uf[r], r = x, self.uf[r]
        return x

    def union(self, x, y):
        self.set |= {x, y}
        ux, uy = self.find(x), self.find(y)
        if ux == uy:
            return
        if self.uf[ux] < self.uf[uy]:
            self.uf[ux] += self.uf[uy]
            self.uf[uy] = ux
        else:
            self.uf[uy] += self.uf[ux]
            self.uf[ux] = uy
        self.count_ -= 1

    def count(self):
        return self.count_


n, m = cin_int_ls()
d = cin_int_ls()
e = []
uf = UnionFind(n)
for _ in range(n - 1):
    uf.union(*cin_int_ls())

if uf.count() == 1:
    print("YES")
else:
    print(uf.count())
