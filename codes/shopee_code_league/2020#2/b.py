import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


class Node:

    def __init__(self, name):
        self.name = name
        self.nxt = {}
        self.parent = None

    def add_next(self, name, weight):
        self.nxt[name] = weight


n = cin_int()
nodes = [Node(i) for i in range(1, n + 1)]
root = nodes[0]
for _ in range(n - 1):
    a, b, w = cin_int_ls()
    nodes[a - 1].add_next(nodes[b - 1], w)
    nodes[b - 1].add_next(nodes[a - 1], w)


def dfs(node):
    top2 = []
    twos = 0
    for nxt, weight in node.nxt.items():
        if node.parent and node.parent == nxt:
            continue
        nxt.parent = node
        two, single = dfs(nxt)
        twos = max(two, twos)
        if len(top2) < 2:
            top2.append(single + weight)
        else:
            top2.append(single + weight)
            top2.sort(reverse=True)
            top2.pop()
    if len(top2) == 0:
        return max(0, twos), 0
    elif len(top2) == 1:
        return max(top2[0], twos), top2[0]
    else:
        return max(twos, top2[0] + top2[1]), top2[1]


# 不知道写对没,有点怀疑自己
ans = dfs(root)
print(ans[0])
