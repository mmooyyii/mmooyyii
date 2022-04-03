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

a + b = (a & b) + (a | b)


逆元

ax === 1 (mod b)
ax === a**(b-1) (mod b)
x === a**(b-2) (mod b)
x = pow(a,b-2,b)
"""

import random
from sys import setrecursionlimit

MOD = 1_000_000_007
setrecursionlimit(int(1e9))


def ex_gcd(a, b):
    return pow(a, b - 2, b)


b = 7249017203 * 129301832
a = 7249017203
p = int(1e9) + 7

a1 = ex_gcd(a, p)

print((b // a) % p, (b * a1) % p)


def is_palindrome(n):
    n = str(n)
    for i in range(len(n) // 2):
        if i > len(n) // 2:
            return True
        if n[i] != n[len(n) - 1 - i]:
            return False
    return True


def next_palindrome(x):
    x = str(x)
    if x == '9' * len(x):
        return int('1' + '0' * (len(x) - 1) + '1')
    if len(x) & 1:
        half = int(x[:len(x) // 2 + 1])
        half = str(half + 1)
        return int(half + half[:-1][::-1])
    else:
        half = int(x[:len(x) // 2])
        half = str(half + 1)
        return int(half + half[::-1])


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


# copy from https://github.com/keon/algorithms/blob/master/algorithms/tree/segment_tree/segment_tree.py
class SegmentTreeOrder:
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

    def query(self, l, r):
        return self.__query(0, 0, len(self.arr) - 1, l, r)


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


def dijkstra(start, g):
    import heapq
    from collections import defaultdict
    heap = [(0, start)]
    ans = defaultdict(lambda: int(1e18))
    ans[start] = 0
    while heap:
        dist, node = heapq.heappop(heap)
        if ans[node] != dist:
            continue
        for nxt, weight in g[node].items():
            if ans[nxt] > ans[node] + weight:
                ans[nxt] = ans[node] + weight
                heapq.heappush(heap, (dist + weight, nxt))
    return ans


class RabinKarp:
    mod = 67280421310721  # int(1e9)+7
    big_primes = [16777619]
    to_int = ord
    # big_primes = [10]
    # to_int = int
    ex_gcd = []
    for i in big_primes:
        ex_gcd.append(pow(i, mod - 2, mod))

    def __init__(self):
        from collections import deque
        self.hash = [0 for _ in RabinKarp.big_primes]
        self.string = deque()

    def append(self, char):
        for i in range(len(RabinKarp.big_primes)):
            self.hash[i] = ((self.hash[i] * RabinKarp.big_primes[i]) + RabinKarp.to_int(char)) % RabinKarp.mod
        self.string.append(char)
        return self

    def appendleft(self, char):
        for i in range(len(RabinKarp.big_primes)):
            self.hash[i] += pow(RabinKarp.big_primes[i], len(self.string), RabinKarp.mod) * RabinKarp.to_int(char)
            self.hash[i] %= RabinKarp.mod
        self.string.appendleft(char)
        return self

    def pop(self):
        char = self.string.pop()
        for i in range(len(RabinKarp.big_primes)):
            self.hash[i] = ((self.hash[i] - RabinKarp.to_int(char)) * RabinKarp.ex_gcd[i]) % RabinKarp.mod
        return self

    def popleft(self):
        char = self.string.popleft()
        for i in range(len(RabinKarp.big_primes)):
            self.hash[i] -= pow(RabinKarp.big_primes[i], len(self.string), RabinKarp.mod) * RabinKarp.to_int(char)
            self.hash[i] %= RabinKarp.mod
        return self

    def hash_value(self):
        return tuple(self.hash)

    def __repr__(self):
        return str({"string": ''.join(self.string), "hash": self.hash_value()})


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
                print(index)
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
        self.primes = self.prime(int(max_value ** 0.5) + 1)

    def prime(self, n):
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

    # 因式分解
    def split(self, n):
        ret = []
        for i in self.primes:
            while n % i == 0:
                n //= i
                ret.append(i)
            if n == 1:
                return ret
            if i >= n:
                break
        ret.append(n)
        return ret


class UnionFind:
    def __init__(self, n):
        from collections import defaultdict
        self.uf = defaultdict(lambda: -1)
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
def next_permutation(nums):
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
            idx = self.data[v]
            idx.append(i)

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


class SegmentSum:

    def __init__(self, ls):
        start = 0
        self.pre = [0]
        for i in ls:
            start += i
            self.pre.append(start)

    def range(self, l, r):
        return self.pre[r] - self.pre[l]


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def makeLeetCodeBinaryTree(data):
    data = [TreeNode(i) if i else None for i in data]
    root = data[0]
    for i, v in enumerate(data):
        if i * 2 + 1 < len(data):
            v.left = data[i * 2 + 1]
        if i * 2 + 2 < len(data):
            v.right = data[i * 2 + 2]
    return root


def topo_sort(g: dict):
    from collections import deque
    node_in = {k: 0 for k in g}
    for k, v in g.items():
        for nxt in v:
            node_in[nxt] += 1
    q = deque()
    for k, v in node_in.items():
        if v == 0:
            q.append(k)
    ans = []
    while len(q):
        a = q.popleft()
        ans.append(a)
        for nxt in g[a]:
            node_in[nxt] -= 1
            if node_in[nxt] == 0:
                q.append(nxt)
    return ans


class LinkedNode:

    def __init__(self, v):
        self.val = v
        self.pre, self.nxt = None, None


def list_to_linked_node(ls):
    head = LinkedNode(None)
    pre = head
    for i in ls:
        node = LinkedNode(i)
        pre.nxt = node
        node.pre = pre
        pre = node
    return head.nxt


def print_link(head):
    while head:
        if head.nxt:
            print(head.val, end=" -> ")
        else:
            print(head.val)
        head = head.nxt


def multi_source_bfs(start, g):
    from collections import deque
    q = deque()
    vis = set()
    used = set()
    for i in start:
        q.append(i)
        used.add(i)
        vis.add(i)
    while q:
        node = q.popleft()
        print(node)
        if node not in used:
            used.add(node)
            for nxt in g[node]:
                if nxt not in vis:
                    vis.add(nxt)
                    q.append(nxt)


### 后缀数组

def sa_naive(s):
    n = len(s)
    sa = list(range(n))
    sa.sort(key=lambda x: s[x:])
    return sa


def sa_doubling(s):
    n = len(s)
    sa = list(range(n))
    rnk = s
    tmp = [0] * n
    k = 1
    while k < n:
        sa.sort(key=lambda x: (rnk[x], rnk[x + k])
        if x + k < n else (rnk[x], -1))
        tmp[sa[0]] = 0
        for i in range(1, n):
            tmp[sa[i]] = tmp[sa[i - 1]]
            if sa[i - 1] + k < n:
                x = (rnk[sa[i - 1]], rnk[sa[i - 1] + k])
            else:
                x = (rnk[sa[i - 1]], -1)
            if sa[i] + k < n:
                y = (rnk[sa[i]], rnk[sa[i] + k])
            else:
                y = (rnk[sa[i]], -1)
            if x < y:
                tmp[sa[i]] += 1
        k *= 2
        tmp, rnk = rnk, tmp
    return sa


def sa_is(s, upper):
    n = len(s)
    if n == 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        if s[0] < s[1]:
            return [0, 1]
        else:
            return [1, 0]
    if n < 10:
        return sa_naive(s)
    if n < 50:
        return sa_doubling(s)
    ls = [0] * n
    for i in range(n - 2, -1, -1):
        ls[i] = ls[i + 1] if s[i] == s[i + 1] else s[i] < s[i + 1]
    sum_l = [0] * (upper + 1)
    sum_s = [0] * (upper + 1)
    for i in range(n):
        if ls[i]:
            sum_l[s[i] + 1] += 1
        else:
            sum_s[s[i]] += 1
    for i in range(upper):
        sum_s[i] += sum_l[i]
        if i < upper:
            sum_l[i + 1] += sum_s[i]
    lms_map = [-1] * (n + 1)
    m = 0
    for i in range(1, n):
        if not ls[i - 1] and ls[i]:
            lms_map[i] = m
            m += 1
    lms = []
    for i in range(1, n):
        if not ls[i - 1] and ls[i]:
            lms.append(i)
    sa = [-1] * n
    buf = sum_s.copy()
    for d in lms:
        if d == n:
            continue
        sa[buf[s[d]]] = d
        buf[s[d]] += 1
    buf = sum_l.copy()
    sa[buf[s[n - 1]]] = n - 1
    buf[s[n - 1]] += 1
    for i in range(n):
        v = sa[i]
        if v >= 1 and not ls[v - 1]:
            sa[buf[s[v - 1]]] = v - 1
            buf[s[v - 1]] += 1
    buf = sum_l.copy()
    for i in range(n - 1, -1, -1):
        v = sa[i]
        if v >= 1 and ls[v - 1]:
            buf[s[v - 1] + 1] -= 1
            sa[buf[s[v - 1] + 1]] = v - 1
    if m:
        sorted_lms = []
        for v in sa:
            if lms_map[v] != -1:
                sorted_lms.append(v)
        rec_s = [0] * m
        rec_upper = 0
        rec_s[lms_map[sorted_lms[0]]] = 0
        for i in range(1, m):
            l = sorted_lms[i - 1]
            r = sorted_lms[i]
            end_l = lms[lms_map[l] + 1] if lms_map[l] + 1 < m else n
            end_r = lms[lms_map[r] + 1] if lms_map[r] + 1 < m else n
            same = True
            if end_l - l != end_r - r:
                same = False
            else:
                while l < end_l:
                    if s[l] != s[r]:
                        break
                    l += 1
                    r += 1
                if l == n or s[l] != s[r]:
                    same = False
            if not same:
                rec_upper += 1
            rec_s[lms_map[sorted_lms[i]]] = rec_upper
        rec_sa = sa_is(rec_s, rec_upper)
        for i in range(m):
            sorted_lms[i] = lms[rec_sa[i]]
        sa = [-1] * n
        buf = sum_s.copy()
        for d in sorted_lms:
            if d == n:
                continue
            sa[buf[s[d]]] = d
            buf[s[d]] += 1
        buf = sum_l.copy()
        sa[buf[s[n - 1]]] = n - 1
        buf[s[n - 1]] += 1
        for i in range(n):
            v = sa[i]
            if v >= 1 and not ls[v - 1]:
                sa[buf[s[v - 1]]] = v - 1
                buf[s[v - 1]] += 1
        buf = sum_l.copy()
        for i in range(n - 1, -1, -1):
            v = sa[i]
            if v >= 1 and ls[v - 1]:
                buf[s[v - 1] + 1] -= 1
                sa[buf[s[v - 1] + 1]] = v - 1
    return sa


def suffix_array(s, upper=255):
    s = [ord(c) for c in s]
    return sa_is(s, upper)


class SuffixArray:

    def __init__(self, s):
        self.sa = suffix_array(s)
        self.rk = self._rk(self.sa)
        self.height = self._height(s)

    def _rk(self, sa):
        rk = [0 for _ in sa]
        for i in range(len(sa)):
            rk[sa[i]] = i
        return rk

    def _height(self, s):
        sa, rk = self.sa, self.rk
        ht = [0] * len(sa)
        k = 0
        for sai in range(0, len(s)):
            if k:
                k -= 1
            while True:
                ai, bi = sai + k, sa[rk[sai] - 1] + k
                if not (0 <= ai < len(s) and 0 <= bi < len(s)):
                    break
                if max(ai, bi) >= len(s):
                    break
                elif s[ai] == s[bi]:
                    k += 1
                else:
                    break
            ht[rk[sai]] = k
        return ht


def draw_graph(edges):
    import networkx as nx
    import matplotlib.pyplot as plt
    edges = [list(map(str, edge)) for edge in edges]
    G = nx.DiGraph()
    for i, v in enumerate(edges):
        a, b = v
        G.add_edge(a, b, id=i + 1)
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_size=500)
    nx.draw(G, pos, with_labels=True, connectionstyle='arc3, rad = 0.1')
    plt.show()


def kanade(ls):
    # 最小子数组
    # print(kanade([-3, -2 - 3]))
    ans = -int(1e9)
    pre = -int(1e9)
    for i in ls:
        pre = max(i, i + pre)
        ans = max(ans, pre)
    return ans


def matrix_pre_sum(data):
    # 矩阵前缀和
    ans = [[0 for _ in range(len(data[0]) + 1)] for _ in range(len(data) + 1)]
    for x in range(len(data)):
        tmp = 0
        for y in range(len(data[0])):
            tmp += data[x][y]
            ans[x][y] = tmp + ans[x - 1][y]
    return ans


def get_sub_matrix(pre, x1, y1, x2, y2):
    # 2边都能取到
    return pre[x2][y2] + pre[x1 - 1][y1 - 1] - pre[x2][y1 - 1] - pre[x1 - 1][y2]


def mex(ls):
    ans = []
    vis = set()
    tmp = 0
    for i in ls:
        vis.add(i)
        while tmp in vis:
            tmp += 1
        ans.append(tmp)
    return ans


class KM:
    INF = int(1e9)

    def __init__(self, graph):
        ma = max(len(graph), len(graph[0]))
        self.graph = graph
        self.vis_x = set()
        self.vis_y = set()
        self.match = [-1] * ma
        self.lx = [max(row) for row in graph]
        self.ly = [0] * ma
        self.slack = []
        self.fa = []

        self.nx, self.ny = len(graph), len(graph[0])

    def find_path(self, x):
        self.vis_x.add(x)
        for y in range(self.ny):
            if y in self.vis_y:
                continue
            tmp_delta = self.lx[x] + self.ly[y] - self.graph[x][y]
            if tmp_delta == 0:
                self.vis_y.add(y)
                self.fa[y + self.nx] = x
                if self.match[y] == -1:
                    return y + self.nx
                self.fa[self.match[y]] = y + self.nx
                res = self.find_path(self.match[y])
                if res > 0:
                    return res
            elif self.slack[x] > tmp_delta:
                self.slack[x] = tmp_delta

        return -1

    def solve(self):
        for x in range(self.nx):
            self.slack = [KM.INF] * self.nx
            self.fa = [-1] * (self.nx + self.ny)
            self.vis_x.clear()
            self.vis_y.clear()
            fir = 1
            leaf = -1
            while True:
                if fir == 1:
                    leaf = self.find_path(x)
                    fir = 0
                else:
                    for i in range(self.nx):
                        if self.slack[i] == 0:
                            self.slack[i] = KM.INF
                            leaf = self.find_path(i)
                            if leaf > 0:
                                break
                if leaf > 0:
                    p = leaf
                    while p > 0:
                        self.match[p - self.nx] = self.fa[p]
                        p = self.fa[self.fa[p]]
                    break
                else:
                    delta = KM.INF
                    for i in range(self.nx):
                        if i in self.vis_x and delta > self.slack[i]:
                            delta = self.slack[i]
                    for i in range(self.nx):
                        if i in self.vis_x:
                            self.lx[i] -= delta
                            self.slack[i] -= delta
                    for j in range(self.ny):
                        if j in self.vis_y:
                            self.ly[j] += delta
        return self.match


class Node:

    def __init__(self, val):
        self.val = val
        self.nxt = set()
