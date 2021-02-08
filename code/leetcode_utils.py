"""
记录一些LeetCode常常会用的的函数与数据结构
"""

import random


def is_palindrome(n):
    n = str(n)
    for i in range(len(n) // 2):
        if i > len(n) // 2:
            return True
        if n[i] != n[len(n) - 1 - i]:
            return False
    return True


a = is_palindrome(1)
print(a)


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
        self.span = 1


class SkipList:

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
            print("Layer: ", end='')
            while node:
                if node.next:
                    print(node.k, end=' -> ')
                else:
                    print(node.k, end='')
                node = node.next
            print()

    def rank(self, n):
        pass


class SegmentTree:

    def __init__(self):
        pass


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


def karp_rabin(pre_hash, string):
    for char in string:
        pre_hash *= 27
        pre_hash += ord(char) - ord('a') + 1
        pre_hash %= 100_000_0007
    return pre_hash


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
