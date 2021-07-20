from typing import *


class MaxXor:
    MaxSize = 4

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
                try:
                    k = list(node.keys())[0]
                    ret += int(k) ^ int(bit)
                    node = node[k]
                except:
                    print(self.root,n)
                    raise RuntimeError

        return ret


class Solution:
    def maxGeneticDifference(self, parents: List[int], queries: List[List[int]]):
        g = {i: set() for i in range(len(parents))}
        g[-1] = set()
        for i, v in enumerate(parents):
            g[v].add(i)
        q = {}
        for node, val in queries:
            q.setdefault(node, {})
            q[node][val] = None

        x = MaxXor()

        def dfs(node):
            x.add(node)
            # print(x.root, node)
            if node in q:
                for k in q[node].keys():
                    q[node][k] = x.get(k)
            for nxt in g[node]:
                dfs(nxt)
            x.remove(node)

        for start in g[-1]:
            dfs(start)
        ret = []
        for node, val in queries:
            ret.append(q[node][val])
        print(ret)
        return ret


Solution().maxGeneticDifference([3, 5, 5, 7, 9, -1, 5, 5, 9, 2],
                                [[3, 34], [2, 46], [9, 36], [7, 15], [7, 26], [3, 6], [1, 42], [6, 22], [6, 26],
                                 [7, 46]])
