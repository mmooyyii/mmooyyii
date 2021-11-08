from typing import *
from functools import lru_cache


class SegmentTree:
    def __init__(self, arr, function):
        self.segment = [0 for x in range(3 * len(arr) + 3)]
        self.arr = arr
        self.fn = function
        self.make_tree(0, 0, len(arr) - 1)

    def make_tree(self, i, l, r):
        if l == r:
            self.segment[i] = self.arr[l]
        elif l < r:
            self.make_tree(2 * i + 1, l, int((l + r) / 2))
            self.make_tree(2 * i + 2, int((l + r) / 2) + 1, r)
            self.segment[i] = self.fn(self.segment[2 * i + 1], self.segment[2 * i + 2])

    def __query(self, i, L, R, l, r):
        if l > R or r < L or L > R or l > r:
            return None
        if L >= l and R <= r:
            return self.segment[i]
        val1 = self.__query(2 * i + 1, L, int((L + R) / 2), l, r)
        val2 = self.__query(2 * i + 2, int((L + R + 2) / 2), R, l, r)
        if val1 is not None:
            if val2 is not None:
                return self.fn(val1, val2)
            return val1
        return val2

    def query(self, L, R):
        return self.__query(0, 0, len(self.arr) - 1, L, R)


def merge(a, b):
    print(a,b)
    return a + b


s = SegmentTree([[i] for i in range(10)], function=merge)
print("-------------------")
print(s.query(1, 2))
print(s.query(6, 7))

