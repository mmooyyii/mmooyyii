import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


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


from collections import defaultdict, Counter

n_city, n_warehouse, n_edges = cin_int_ls()
graph = defaultdict(dict)
for _ in range(n_edges):
    a, b = cin_int_ls()
    graph[a][b] = 1
    graph[b][a] = 1

a = floyd(n_city + 1, graph)
for i in a:
    print(i)

for _ in range(n_warehouse):
    dto, fee, city = cin_int_ls()

custom = Counter()
for _ in range(cin_int()):
    n, city = cin_int_ls()
    custom[city] += n
print(custom)
