import sys
from sortedcontainers import SortedList


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


# https://codeforces.com/blog/entry/87287

def solve1():
    n, k = cin_int_ls()
    ls = cin_int_ls()
    ls = [i - k for i in ls]

    ans = 0
    pre = [0]
    for i in ls:
        pre.append(pre[-1] + i)
    sl = SortedList()
    sl.add(0)
    for i in pre[1:]:
        ans += sl.bisect_right(i)
        sl.add(i)
    print(ans)


