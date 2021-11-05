"""
记录一些LeetCode常常会用的的函数与数据结构
"""
"""
# 绝对值展开，也许可以简化计算
# abs(a-b) + abs(c-d) = max{a-b + (c-d),-a+b + (c-d),a-b + (-c+d),-a+b + (-c+d)}

# 验证答案需要O(n)的情况下，考虑使用二分法
# 离线查询的情况下，记得可以调整查询的顺序

a / b = c 
a % b = c 
a ^ b = c
这种情况 遍历a c 会比 遍历 a b更快


费马小定理
若 p 为素数 gcd(a,p)==1，则 a^(p-1) === 1 mod p
另一个形式：对于任意整数 a ，有 a^p === a mod p

if MartixA @ MartixB = MartixC
then MartixC @ np.linag.inv(MatrixA) = MatrixB
"""

import math
import random
from sys import setrecursionlimit
import bisect
from typing import *
import collections

MOD = 1_000_000_007

setrecursionlimit(int(1e9))


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


class SegmentTree:

    def __init__(self, ls, calc=lambda x, y: x + y):
        def f(a, b):
            if a is None:
                return b
            elif b is None:
                return a
            else:
                return calc(a, b)

        self.data = ls
        self.calc = f
        self.tree = [0 for _ in range(len(ls) * 4)]
        for i, v in enumerate(ls):
            self.tree[i + len(self.data)] = v
        for i in range(len(ls) - 1, 0, -1):
            self.tree[i] = self.calc(self.tree[i * 2], self.tree[i * 2 + 1])

    def __setitem__(self, key, value):
        self.data[key] = value
        pos = key + len(self.data)
        self.tree[pos] = value
        while pos:
            left, right = pos, pos
            if pos & 1:
                left = pos - 1
            else:
                right = pos + 1
            pos >>= 1
            self.tree[pos] = self.calc(self.tree[left], self.tree[right])

    def range(self, left, right):  # 左右都能取到
        rt = None
        left += len(self.data)
        right += len(self.data)
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


def dijkstra2(start, g):
    import heapq
    vis = {}
    heap = [(0, start)]
    vis[start] = 0
    ret = {}
    while heap:
        dist, node = heapq.heappop(heap)
        ret.setdefault(node, float('inf'))
        ret[node] = min(ret[node], dist)
        for n, weight in g[node].items():
            if n not in vis or (n in vis and vis[n] > dist + weight):
                vis[n] = dist + weight
                heapq.heappush(heap, (dist + weight, n))
    return ret


def dijkstra(start, end, g):
    import heapq
    vis = {}
    heap = [(0, start)]
    vis[start] = 0
    while heap:
        dist, node = heapq.heappop(heap)
        if node == end:
            return dist
        if vis[node] < dist:
            continue
        for n, weight in g[node].items():
            if n not in vis or (n in vis and vis[n] > dist + weight):
                vis[n] = dist + weight
                heapq.heappush(heap, (dist + weight, n))
    return -1


class KarpRabin:
    big_primes = [16777619, 17]
    maxInt = 1 << 32

    def __init__(self, string, n):
        if n > len(string):
            raise ValueError
        self.length = 0
        self.hash = [0 for _ in KarpRabin.big_primes]
        self.s = string
        self.n = n
        self.to_int = int
        self.sub_memo = {}
        for char in string[:n]:
            self.add_tail(char)

    def add_tail(self, char):
        for i in range(len(KarpRabin.big_primes)):
            self.hash[i] *= KarpRabin.big_primes[i]
            self.hash[i] += self.to_int(char)
            self.hash[i] %= KarpRabin.maxInt
        self.length += 1

    def sub_head(self, char):
        for i in range(len(KarpRabin.big_primes)):
            key = (self.length - 1, i)
            if key in self.sub_memo:
                sub = self.sub_memo[key]
            else:
                sub = 1
                for _ in range(self.length - 1):
                    sub *= KarpRabin.big_primes[i]
                    sub %= KarpRabin.maxInt
                self.sub_memo[key] = sub
            sub *= self.to_int(char)
            sub %= KarpRabin.maxInt
            self.hash[i] += KarpRabin.maxInt
            self.hash[i] -= sub
            self.hash[i] %= KarpRabin.maxInt
        self.length -= 1

    def scan(self):
        yield tuple(self.hash)
        for i in range(len(self.s) - self.n):
            tail = self.s[i + self.n]
            self.add_tail(tail)
            head = self.s[i]
            self.sub_head(head)
            yield tuple(self.hash)


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


def miller_rabin(p):
    """
    费马小定理
    若 p 为素数 gcd(a,p)==1，则 a^(p-1) === 1 mod p
    另一个形式：对于任意整数 a ，有 a^p === a (mod p)
    """
    if p < 3:
        return p == 2
    for _ in range(8):
        if pow(random.randint(2, p - 1), p - 1, p) != 1:
            return False
    return True


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


class SpiltPrime:

    def __init__(self, max_value):
        self.prime = prime(int(max_value ** 0.5) + 1)

    # 因式分解
    def split(self, n):
        ret = []
        for i in self.prime:
            while n % i == 0:
                n //= i
                ret.append(i)
            if n == 1 or i > n:
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


class RangeCount:
    # 范围内某个数的个数： index倒排 + 二分查找  空间O(n) 时间O(logN)
    def __init__(self, ls):
        ma = max(ls)
        self.data = [[] for _ in range(ma + 1)]
        for i, v in enumerate(ls):
            self.data[v].append(i)

    def count(self, lo, hi, v):
        return binary_search_lte(hi, self.data[v]) - binary_search_lt(lo, self.data[v])


def single_stack(ls):
    stack = []
    ret = []
    for i in ls[::-1]:
        while stack and stack[-1] <= i:
            stack.pop()
        if not stack:
            ret.append(-1)
        else:
            ret.append(stack[-1])
        stack.append(i)
    ret.reverse()
    return ret


# 大鸟转转转
def roll_roll_roll(matrix, n, depth):
    maxx, maxy = len(matrix) - 1 - depth, len(matrix[0]) - 1 - depth

    def nxt(x, y):
        if y == depth and depth <= x < maxx:
            return x + 1, y
        if x == maxx and depth <= y < maxy:
            return x, y + 1
        if y == maxy and depth < x <= maxx:
            return x - 1, y
        if x == depth and depth < y <= maxy:
            return x, y - 1
        return x, y

    x, y = depth, depth
    tmp = []
    while True:
        tmp.append(matrix[x][y])
        x, y = nxt(x, y)
        if (x, y) == (depth, depth):
            break
    n %= len(tmp)
    # n = len(tmp) - n # 逆时针或顺时针
    tmp = tmp[n:] + tmp[:n]
    x, y = depth, depth
    print(tmp)
    for i in tmp:
        matrix[x][y] = i
        x, y = nxt(x, y)
    for row in matrix:
        print(row)


def hungary(girls_expect, boys, girls):
    """
    graph: {girl1: {boy1,boy2....}}
    boys: the number of boys
    girls: the number of girls
    """

    boys_expect = {i: set() for i in range(boys)}
    for girl, boysList in girls_expect.items():
        for boy in boysList:
            boys_expect[boy].add(girl)

    def find(boy):
        for girl in boys_expect[boy]:
            if tried[girl] == 0:
                tried[girl] = 1
                if girl not in girl_choice or find(girl_choice[girl]):
                    girl_choice[girl] = boy
                    return True
        return False

    girl_choice = [-1 for _ in range(girls)]
    for boy in range(boys):
        tried = [0 for _ in range(girls)]
        find(boy)

    return girl_choice


class MaxXor:
    MaxSize = 16

    def __init__(self):
        self.root = {}
        self.count = {}

    def add(self, n):
        self.count.setdefault(n, 0)
        self.count[n] += 1
        b = bin(n)[2:]
        b = '0' * (MaxXor.MaxSize - len(b)) + b
        node = self.root
        for bit in b:
            node = node.setdefault(bit, {})

    def remove(self, n):
        self.count[n] -= 1
        if self.count[n] == 0:
            print('before', n, self.root)
            b = bin(n)[2:]
            b = '0' * (MaxXor.MaxSize - len(b)) + b
            node = self.root
            chain = []
            for bit in b:
                chain.append([bit, node])
                node = node.setdefault(bit, {})

            while chain:
                bit, node = chain.pop()
                if node[bit] == {}:
                    node.pop(bit)
            print('after', n, self.root)

    def get(self, n):
        b = bin(n)[2:]
        b = '0' * (MaxXor.MaxSize - len(b)) + b
        node = self.root
        ret = 0
        for bit in b:
            ret <<= 1
            if len(node) == 2:
                ret += 1
                if bit == '0':
                    node = node['1']
                else:
                    node = node['0']
            else:
                k = list(node.keys())[0]
                ret += int(k) ^ int(bit)
                node = node[k]
        return ret


def dot(matrix1, matrix2):
    if len(matrix1[0]) != len(matrix2):
        raise ValueError
    ans = [[0 for _ in matrix2[0]] for _ in matrix1]
    for x in range(len(ans)):
        for y in range(len(ans[0])):
            for i in range(len(matrix1[0])):
                ans[x][y] += matrix1[x][i] * matrix2[i][y]

    return ans


p = [[0, 1], [1, 1]]
a = [[1, 1]]


def q_pow(matrix, b):
    ans = matrix
    b -= 1
    while b > 0:
        if b & 1:
            ans = dot(ans, matrix)
        matrix = dot(matrix, matrix)
        b >>= 1
    return ans


def rank(ls):
    rk = [0 for _ in ls]
    ls = [(v, i) for i, v in enumerate(ls)]
    ls.sort()
    pre = 0
    for i in range(len(ls)):
        r = i
        if ls[i - 1][0] == ls[i][0]:
            r = pre
        idx = ls[i][1]
        rk[idx] = r
        pre = r
    return rk


def suffix_array(s):
    rk = rank(s)
    skip = 1
    while skip < len(s):
        source = [[0, 0] for _ in s]
        for i in range(len(s)):
            source[i][0] = rk[i]
            if i + skip < len(s):
                source[i][1] = rk[i + skip]
        rk = rank(source)
        skip *= 2
    sa = [0 for _ in s]
    for i in range(len(s)):
        sa[rk[i]] = i
    return sa, rk


sa, rk = suffix_array("ababa")
print(*map(lambda x: x + 1, sa))

# 数论分块
def slow(n):
    ans = 0
    for i in range(1, n + 1):
        ans += n // i
    return ans


def quick(n):
    ans = 0
    l, r = 1, 0
    while l <= n:
        r = n // (n // l)
        ans += (r - l + 1) * (n // l)
        l = r + 1
    return ans

