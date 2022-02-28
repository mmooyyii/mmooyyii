import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


class Node:

    def __init__(self, item):
        self.type = 0  # 0 Dynamic,1 Fix
        self.stock = 0
        self.item = item
        self.qty = 0


def main():
    n, m = cin_int_ls()
    nodes = {i: Node(i) for i in range(1, n + 1)}
    nodes[1].stock = m
    nodes[1].type = 1
    for i in range(n - 1):
        item = i + 2
        cmd = cin_int_ls()
        if len(cmd) == 3:
            _, parent, qty = cmd
            add = nodes[item]
            add.type = 1
        else:
            _, parent, qty, s = cmd
