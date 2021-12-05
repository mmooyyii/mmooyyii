from typing import *
import random


class UnionFind:
    def __init__(self):
        from collections import defaultdict
        self.uf = defaultdict(lambda: -1)
        self._count = 0

    def find(self, x):
        r = x
        while self.uf[x] >= 0:
            x = self.uf[x]
        while r != x:
            self.uf[r], r = x, self.uf[r]
        return x

    def union(self, x, y):
        ux, uy = self.find(x), self.find(y)
        if ux == uy:
            return
        if ux <= 0 and uy <= 0:
            self._count += 1
        if self.uf[ux] < self.uf[uy]:
            self.uf[ux] += self.uf[uy]
            self.uf[uy] = ux
        else:
            self.uf[uy] += self.uf[ux]
            self.uf[ux] = uy

    def count(self):
        return self._count

    def group_by(self):
        pass


uf = UnionFind()
uf.union(1, 2)
uf.union(2, 3)
print(uf.uf)
print(uf.count())
