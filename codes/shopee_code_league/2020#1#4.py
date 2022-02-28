import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


from functools import lru_cache


@lru_cache(None)
def dp(idx, k):
    if idx == len(items):
        return 0 if k == 0 else -int(1e18)
    if k == 0:
        return 0
    return max(
        dp(idx + 1, k - 1) + items[idx],
        dp(idx + 1, k),
    )


# 这题有点白给啊
n, k = cin_int_ls()
items = []
for _ in range(n):
    ls = cin_int_ls()
    ls.sort()
    items.append(ls[-1] + ls[-2])
ans = dp(0, k)
print(ans)
