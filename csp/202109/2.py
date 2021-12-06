import sys

sys.setrecursionlimit(int(1e9))


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


class LinkedNode:

    def __init__(self, v):
        self.val = v
        self.pre, self.nxt = None, None


MAX = int(1e4) + 1


def main():
    cin_int()
    ls = cin_int_ls()
    head = None
    pre = head
    memo = [[] for _ in range(MAX)]
    for i in ls:
        node = LinkedNode(i)
        memo[i].append(node)
        if head is None:
            head = node
        if pre:
            pre.nxt = node
        node.pre = pre
        pre = node
    ans = 0
    count = 1
    for i in range(0, MAX):
        for node in memo[i]:
            if node.nxt and node.pre:
                count += 1
            elif (not node.nxt) and (not node.pre):
                count -= 1
            if node.nxt:
                node.nxt.pre = None
            if node.pre:
                node.pre.nxt = None
        ans = max(ans, count)
    print(ans)


main()
