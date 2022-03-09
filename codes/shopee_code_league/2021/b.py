import sys
from sortedcontainers import SortedList


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


# https://codeforces.com/blog/entry/87287

n, k = cin_int_ls()
ls = cin_int_ls()
ls = [i - k for i in ls]

sl = SortedList()
ans = 0
pre = 0
for i in ls:
    if i >= 0:
        ans += 1
    pre += i
    rk = sl.bisect_left(pre)
    ans += len(sl) - rk
    sl.add(pre)

print(ans)
