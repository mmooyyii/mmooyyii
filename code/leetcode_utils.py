"""
记录一些LeetCode常常会用的的函数与数据结构
"""
import math
import random
from sys import setrecursionlimit
import bisect

import collections

setrecursionlimit(9999999)
MOD = 1_000_000_007


def is_palindrome(n):
    n = str(n)
    for i in range(len(n) // 2):
        if i > len(n) // 2:
            return True
        if n[i] != n[len(n) - 1 - i]:
            return False
    return True


def binary_search_lte(target: int, ls: list) -> int:
    # 返回小于等于target的个数
    left, right = 0, len(ls)
    while left < right:
        mid = (right + left) // 2
        if ls[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left


def binary_search_lt(target: int, ls: list) -> int:
    # 返回小于target的个数
    left, right = 0, len(ls)
    while left < right:
        mid = (right + left) // 2
        if ls[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left


def binary_closest(target, ls):
    n = binary_search_lte(target, ls)
    if n == len(ls):
        return ls[-1]
    if ls[n] == target:
        return target
    if abs(target - ls[n]) < abs(target - ls[n - 1]):
        return ls[n]
    return ls[n - 1]


# B个里挑A个，不管顺序有几种情况
# 备注：递推公式：c(a,b) = c(a-1,b-1) + c(a,b-1)
def c(a, b):
    b = min(b, a - b)
    d, m = 1, 1
    for i in range(b):
        d *= i + 1
        m *= a - i
    return m // d


# 排列组合
def comb(elements, n):
    import itertools
    for i in itertools.combinations(elements, n):
        print(i)


# 阶乘
def factorial(n):
    ret = 1
    for i in range(1, n + 1):
        ret *= i
    return ret


# 等比数列求和,q为整数
def sum_a(a1, length, q):
    return int(a1 * (1 - q ** length) / (1 - q))


class Trie:

    def __init__(self):
        self.root = {}

    def add(self, word):
        node = self.root
        for i in word:
            node = node.setdefault(i, {})
        node['is_word'] = True

    def __contains__(self, word):
        node = self.root
        for i in word:
            node = node.setdefault(i, {})
        return node.setdefault('is_word', False)


class SkipListNode:

    def __init__(self, k=float('-inf')):
        self.k = k
        self.next = None
        self.down = None


class SkipList:
    """
    There are 4 kind of SkipListNode

    1) [next] # first node in every layer
    2) [k,next] # mid node without down pointer
    3) [k,next,down] # mid node with down pointer
    4) [k,next,v] # leaf node

    table example
    Layer1: root->          2
                            |
    Layer2: root->          2 -> 3
                            |    |
    Layer3: root->          2 -> 3     ->       6
                            |    |              |
    Layer4: root->0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7
    """

    def __init__(self):

        self.high = 1
        self.root = SkipListNode()
        self.kv = {}

    def add(self, score, member):
        if member in self.kv:
            self.remove(member)
        d = self.depth()
        if d > self.high:
            self._extend_layer(d)
        node = self.root
        pre_new_node = None
        for depth in range(self.high, 0, -1):
            node = self.search_in_layer(node, score)
            if d >= depth:
                new_node = SkipListNode(score)
                new_node.next = node.next
                node.next = new_node
                if pre_new_node:
                    pre_new_node.down = new_node
                pre_new_node = new_node
            node = node.down
        self.kv[member] = score

    @staticmethod
    def search_in_layer(node, k):
        while node.next:
            if node.k <= k <= node.next.k:
                return node
            else:
                node = node.next
        return node

    def _extend_layer(self, d):
        root = self.root
        new_root = None
        pre_layer_head = None
        for _ in range(d - self.high):
            layer_head = SkipListNode()
            if not new_root:
                new_root = layer_head
            if pre_layer_head:
                pre_layer_head.down = layer_head
            pre_layer_head = layer_head
        if pre_layer_head:
            pre_layer_head.down = root
        if new_root:
            self.root = new_root
        self.high = max(self.high, d)

    def remove(self, k):
        if k in self:
            self.kv.pop(k)

    @staticmethod
    def depth():
        d = 1
        while True:
            if random.random() > 0.5:
                return d
            else:
                d += 1

    def show(self):
        head = self.root
        while head:
            node = head.next
            head = head.down
            print("Layer: root->", end='')
            while node:
                if node.next:
                    print(node.k, end=' -> ')
                else:
                    print(node.k, end='')
                node = node.next
            print()

    def rank(self, n):
        pass


s = SkipList()
for i in range(8):
    s.add(i, i)
print(s.show())


class SegmentTree:

    def __init__(self, ls, calc=lambda x, y: x + y):
        self.data = ls
        self.calc = calc
        self.tree = [0 for _ in range(len(ls) * 4)]
        for i, v in enumerate(ls):
            self.tree[i + len(self.data)] = v
        for i in range(len(ls) - 1, 0, -1):
            self.tree[i] = self.calc(self.tree[i * 2], self.tree[i * 2 + 1])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value
        pos = key + len(self)
        self.tree[pos] = value
        while pos:
            left, right = pos, pos
            if pos & 1:
                left = pos - 1
            else:
                right = pos + 1
            pos >>= 1
            self.tree[pos] = self.calc(self.tree[left], self.tree[right])

    def range(self, left, right):
        # 左右都能取到
        rt = 0
        left += len(self)
        right += len(self)
        while left <= right:
            if left & 1:
                rt = self.calc(rt, self.tree[left])
                left += 1
            if not right & 1:
                rt = self.calc(rt, self.tree[right])
                right -= 1
            left >>= 1
            right >>= 1
        return rt


a = SegmentTree([1, 2, 3, 4, 3, 2, 1], min)


def init_digraph(n, edges):
    g = {i: {} for i in range(n)}
    for a, b in edges:
        g[a][b] = 1
    return g


def init_graph(n, edges):
    g = {i: {} for i in range(n)}
    for a, b in edges:
        g[a][b] = 1
        g[b][a] = 1
    return g


# 任意2点间的距离
def floyd(n, g: dict):
    ret = [[float('inf') for _ in range(n)] for _ in range(n)]
    for node, route in g.items():
        ret[node][node] = 0
        for v, w in route.items():
            ret[node][v] = w
            ret[v][node] = w
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if ret[i][j] > ret[i][k] + ret[k][j]:
                    ret[i][j] = ret[i][k] + ret[k][j]
    return ret


def dijkstra(start, end, g):
    import heapq
    heap = [(0, start)]
    while heap:
        dist, node = heapq.heappop(heap)
        for n, weight in g[node].items():
            if n == end:
                return dist + weight
            else:
                heapq.heappush(heap, (dist + weight, n))
    return -1


# karp_rabin


class KarpRabin:
    big_prime = 16777619
    int64 = 1 << 64

    def __init__(self, string):
        self.length = len(string)
        self.hash = 0
        for char in string:
            self.hash *= KarpRabin.big_prime
            self.hash += ord(char)
            self.hash %= KarpRabin.int64

    def add_tail(self, char):
        self.hash *= KarpRabin.big_prime
        self.hash += ord(char)
        self.hash %= KarpRabin.int64
        self.length += 1

    def sub_head(self, char):
        sub = ord(char)
        for _ in range(self.length - 1):
            sub *= KarpRabin.big_prime
            sub %= KarpRabin.int64
        self.hash += KarpRabin.int64
        self.hash -= sub
        self.hash %= KarpRabin.int64
        self.length -= 1


# python 的 str() in str() 也是O(n)
def boyer_moore(pattern, text):
    bad_skip = {}
    good_skip = 0
    for i, v in enumerate(pattern):
        bad_skip[v] = i
    while True:
        if pattern[good_skip] == pattern[-good_skip - 1]:
            good_skip += 1
        else:
            break
    index = 0
    while index + len(pattern) <= len(text):
        search = len(pattern)
        while True:
            search -= 1
            if pattern[search] != text[index + search]:
                suffix_length = len(pattern) - 1 - search
                if text[index + search] in bad_skip:
                    bad = len(pattern) - bad_skip[text[index + search]] - 1
                else:
                    bad = len(pattern) - suffix_length
                if 0 < suffix_length <= good_skip:
                    good = len(pattern) - suffix_length
                elif suffix_length > good_skip:
                    good = len(pattern) - good_skip
                else:
                    good = 0
                break
            if search == 0:
                return True
        index += max(bad, good)
    return False


def prime(n):
    memo = [1 for _ in range(n)]
    ret = []
    for i in range(2, n):
        if memo[i]:
            ret.append(i)
        j = 0
        while j < len(ret) and i * ret[j] < n:
            memo[i * ret[j]] = False
            if i % ret[j] == 0:
                break
            j += 1
    return ret


class UnionFind:
    def __init__(self, n):
        self.uf = [-1 for _ in range(n)]
        self.count_ = n

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
        if self.uf[ux] < self.uf[uy]:
            self.uf[ux] += self.uf[uy]
            self.uf[uy] = ux
        else:
            self.uf[uy] += self.uf[ux]
            self.uf[ux] = uy
        self.count_ -= 1

    def count(self):
        return self.count_


def bucket_sort(ls):
    mi = min(ls)
    ma = max(ls)
    size = ((ma - mi) // (len(ls) - 1)) + 1
    buckets = [[] for _ in ls]
    for n in ls:
        bucket = (n - mi) // size
        buckets[bucket].append(n)
    ret = []
    for bucket in buckets:
        bucket.sort()
        for i in bucket:
            ret.append(i)
    return ret


from functools import lru_cache


@lru_cache(None)
def dp():
    return 0


dp.cache_clear()

#  字典顺的下一个
def nextPermutation(nums):
    if len(nums) <= 1:
        return
    for i in range(len(nums) - 2, -1, -1):
        if nums[i] < nums[i + 1]:
            for k in range(len(nums) - 1, i, -1):
                if nums[k] > nums[i]:
                    nums[i], nums[k] = nums[k], nums[i]
                    nums[i + 1:] = sorted(nums[i + 1:])
                    return
        elif i == 0:
            nums.sort()
    raise ValueError

# 绝对值展开，也许可以简化计算
# abs(a-b) + abs(c-d) = max{a-b + (c-d),-a+b + (c-d),a-b + (-c+d),-a+b + (-c+d)}

# 验证答案需要O(n)的情况下，考虑使用二分法
# 离线查询的情况下，记得可以调整查询的顺序

