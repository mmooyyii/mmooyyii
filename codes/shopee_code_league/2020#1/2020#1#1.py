import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


# 看不懂题目

class Node:

    def __init__(self, val):
        self.children = set()
        self.val = val


def make_balance_random_tree(size):
    import random
    nodes = [Node(i) for i in range(size)]
    random.shuffle(nodes)

    for i, node in enumerate(nodes):
        if i * 2 + 1 < len(nodes):
            node.children.add(nodes[i * 2 + 1])
        if i * 2 + 2 < len(nodes):
            node.children.add(nodes[i * 2 + 2])
    return nodes[0]


root = make_balance_random_tree(4)


def dfs(root):
    trace = []
    ans = []

    def _dfs(cur):
        if len(cur.children) == 0:
            ans.append(trace.copy())
        for nxt in cur.children:
            trace.append(nxt.val)
            _dfs(nxt)
            trace.pop()

    trace.append(root.val)
    _dfs(root)
    trace.pop()
    return ans


a = dfs(root)
print(a)
