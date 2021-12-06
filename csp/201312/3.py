import sys

sys.setrecursionlimit(int(1e9))


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


def main():
    cin_int()
    ls = cin_int_ls()
    stack = []
    lr = [[0, 0] for _ in ls]
    for i, v in enumerate(ls):
        while stack and stack[-1][1] > v:
            idx, _ = stack.pop()
            lr[idx][1] = i
        stack.append([i, v])
    for idx, _ in stack:
        lr[idx][1] = len(ls)
    stack = []
    for i in range(len(ls) - 1, -1, -1):
        v = ls[i]
        while stack and stack[-1][1] > v:
            idx, _ = stack.pop()
            lr[idx][0] = i + 1
        stack.append([i, v])
    for idx, _ in stack:
        lr[idx][0] = 0
    ans = 0
    for i, v in enumerate(lr):
        l, r = v
        ans = max(ans, (r - l) * ls[i])
    print(ans)


main()
