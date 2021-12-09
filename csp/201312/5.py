import sys

sys.setrecursionlimit(int(1e9))


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


def main():
    def nxt(x, y):
        ans = []
        if mat[x][y] == '+' or mat[x][y] == 'S':
            ans = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
        elif mat[x][y] == '-':
            ans = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
        elif mat[x][y] == '|':
            ans = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
        elif mat[x][y] == '.':
            ans = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
        for nx, ny in ans:
            if 0 <= nx < len(mat) and 0 <= ny < len(mat[0]) and mat[nx][ny] != '#':
                yield nx, ny

    from functools import lru_cache

    vis = set()

    @lru_cache(None)
    def dp(x, y):
        vis.add((x, y))
        if x == sx and y == sy:
            return False, True
        if x == ex and y == ey:
            return False, True
        a, b = False, False
        for nx, ny in nxt(x, y):
            if (nx, ny) not in vis:
                vis.add((nx, ny))
                aa, bb = dp(nx, ny)
                a = a or aa
                b = b or bb
        if (a, b) == (True, False):
            ans.add((x, y))
        return a, b

    ans = set()
    x, y = cin_int_ls()
    mat = []
    sx, sy = 0, 0
    ex, ey = 0, 0
    for yy in range(y):
        row = input()
        if row.find('S') != -1:
            sx, sy = yy, row.find('S')
        if row.find('T') != -1:
            ex, ey = yy, row.find('T')
        mat.append(row)
    for x in range(len(mat)):
        for y in range(len(mat[0])):
            dp(x, y)
    for x in range(len(mat)):
        for y in range(len(mat[0])):
            dp(x, y)
    print(ans)


main()

"""
5 5
--+-+
..|#.
..|##
S-+-T
####.
"""
