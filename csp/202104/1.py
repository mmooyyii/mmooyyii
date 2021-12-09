import sys

sys.setrecursionlimit(int(1e9))


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


def main():
    a, b, L = cin_int_ls()
    ans = [0] * L
    for _ in range(a):
        for i in cin_int_ls():
            ans[i] += 1
    print(*ans)


main()
