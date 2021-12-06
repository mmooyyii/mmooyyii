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
    from itertools import groupby

    ma = sum(ls)
    mi = 0
    for i, _ in groupby(ls):
        mi += i
    print(ma)
    print(mi)


main()
