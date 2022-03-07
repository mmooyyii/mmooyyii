import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


from collections import defaultdict

n_city, n_warehouse, n_edges = cin_int_ls()
graph = defaultdict(set)
for _ in range(n_edges):
    a, b = cin_int_ls()
    graph[a].add(b)
    graph[b].add(a)

for _ in range(n_warehouse):
    dto, fee, city = cin_int_ls()

custom = []
for _ in range(cin_int()):
    n, city = cin_int_ls()

# 网络流? 不太会,要去学习一下
