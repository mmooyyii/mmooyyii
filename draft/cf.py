import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


for _ in range(cin_int()):
    n, m, start_x, start_y, end_x, end_y = cin_int_ls()
    ans = 0
    dx, dy = 1, 1
    loop = [(start_x, start_y)]
    while True:
        if (start_x + dx, start_y + dy) in ((0, 0), (0, m + 1), (n + 1, 0), (n + 1, m + 1)):
            dx, dy = -dx, -dy
        elif start_x + dx == n + 1:
            dx, dy = -dx, dy
        elif start_y + dy == m + 1:
            dx, dy = dx, -dy
        elif start_x + dx == 0:
            dx, dy = -dx, dy
        elif start_y + dy == 0:
            dx, dy = dx, -dy
        start_x += dx
        start_y += dy
        loop.append((start_x, start_y))
        if loop[0] == loop[-1]:
            break
