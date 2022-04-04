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


def sv(n, m, d, edges):
    dsu = UnionFind(n)
    for x, y in edges:
        d[x] -= 1
        d[y] -= 1
        dsu.union(x, y)
    temp = [[] for _ in range(n)]
    for i in range(n):
        if d[i] < 0:
            return -1
        temp[dsu.find(i)].extend([i] * d[i])
    c1 = []
    c2 = []
    for i in range(n):
        if len(temp[i]) == 1:
            c1.append(temp[i][0])
        elif len(temp[i]) > 1:
            c2.append(temp[i])
    ans = []
    for v in c2:
        for i in range(0, len(v) - 1):
            if not c1:
                return -1
            aa = c1.pop()
            ans.append([v[i], aa])
            dsu.union(v[i], aa)
        c1.append(v[-1])
    if len(c1) != 2:
        return -1
    dsu.union(c1[0], c1[1])
    ans.append([c1[0], c1[1]])
    if len(dsu.set) != n:
        return -1
    return ans


if __name__ == '__main__':
    n, m = cin_int_ls()
    d = cin_int_ls()
    edges = [list(map(lambda x: x - 1, cin_int_ls())) for _ in range(m)]
    ans = sv(n, m, d, edges)
    if ans == -1:
        print(-1)
    else:
        for a, b in ans:
            print(a + 1, b + 1)
