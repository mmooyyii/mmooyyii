import sys

sys.setrecursionlimit(int(1e9))


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


def nxt_T(x, y):
    ans = []
    if mat[x][y] == '.':
        ans = [[1, 0]]
    elif mat[x][y] in '+ST':
        ans = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    elif mat[x][y] == '-':
        ans = [[0, 1], [0, -1]]
    elif mat[x][y] == '|':
        ans = [[1, 0], [-1, 0]]
    for dx, dy in ans:
        if 0 <= x + dx < len(mat) and 0 <= y + dy < len(mat[0]) and mat[x + dx][y + dy] != '#':
            yield x + dx, y + dy


def nxt_R(x, y):
    ans = []
    dx, dy = 1, 0
    if 0 <= x + dx < len(mat) and 0 <= y + dy < len(mat[0]) and mat[x + dx][y + dy] in 'S+|':
        ans.append([x + dx, y + dy])
    dx, dy = -1, 0
    if 0 <= x + dx < len(mat) and 0 <= y + dy < len(mat[0]) and mat[x + dx][y + dy] in 'S+|.':
        ans.append([x + dx, y + dy])
    dx, dy = 0, 1
    if 0 <= x + dx < len(mat) and 0 <= y + dy < len(mat[0]) and mat[x + dx][y + dy] in 'S+-':
        ans.append([x + dx, y + dy])
    dx, dy = 0, -1
    if 0 <= x + dx < len(mat) and 0 <= y + dy < len(mat[0]) and mat[x + dx][y + dy] in 'S+-':
        ans.append([x + dx, y + dy])
    return ans


mat = []


def main():
    def dfs(x, y):
        for nx, ny in nxt_T(x, y):
            if (nx, ny) not in toS:
                toS.add((nx, ny))
                dfs(nx, ny)

    def dfs2(x, y):
        for nx, ny in nxt_R(x, y):
            if (nx, ny) not in toT:
                toT.add((nx, ny))
                dfs2(nx, ny)

    a, b = cin_int_ls()
    sx, sy = 0, 0
    tx, ty = 0, 0
    for i in range(a):
        row = input()
        if row.find('S') != -1:
            sx, sy = i, row.find('S')
        if row.find('T') != -1:
            tx, ty = i, row.find('T')
        mat.append(row)
    toS = {(sx, sy)}
    dfs(sx, sy)
    if (tx, ty) not in toS:
        print("I'm stuck!")
    toT = {(tx, ty)}
    dfs2(tx, ty)
    ans = toS - toT
    print(len(ans))


main()
