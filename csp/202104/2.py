import sys

sys.setrecursionlimit(int(1e9))


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


def main():
    a, _, r, t = cin_int_ls()
    mat = [[0] * (a + 1)]

    for _ in range(a):
        row = [0]
        pre = [0]
        for i, v in enumerate(cin_int_ls()):
            pre.append(pre[-1] + v)
            row.append(pre[-1] + mat[-1][i + 1])
        mat.append(row)
    ans = 0
    for x in range(len(mat) - 1):
        for y in range(len(mat[0]) - 1):
            lx, ly = max(x - r, 0), max(y - r, 0)
            rx, ry = min(x + r + 1, a), min(y + r + 1, a)
            v = mat[rx][ry] - mat[rx][ly] - mat[lx][ry] + mat[lx][ly]
            if v <= t * abs(rx - lx) * abs(ly - ry):
                ans += 1
    print(ans)


main()
