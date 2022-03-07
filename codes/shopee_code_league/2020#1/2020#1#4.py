import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


from functools import lru_cache


# 扫描线dp O(2^3 * n * k)

@lru_cache(None)
def dp(baseline, a, b, c, k):
    if k == 0:
        return 0
    if baseline == len(items):
        return 0 if k == 0 else -int(1e9)
    mi = min(a, b, c)
    if mi != 0:
        return dp(baseline + mi, a - mi, b - mi, c - mi, k)
    ans = 0
    if baseline == len(items) - 1:  # 只能放横的
        ans = 0
    else:
        if a == 0:
            ans = max(
                dp(baseline, a + 1, b, c, k),
                dp(baseline, a + 2, b, c, k - 1) + items[baseline][0] + items[baseline + 1][0],
            )
        elif b == 0:
            ans = max(
                dp(baseline, a, b + 1, c, k),
                dp(baseline, a, b + 2, c, k - 1) + items[baseline][1] + items[baseline + 1][1],
            )
        elif c == 0:
            ans = max(
                dp(baseline, a, b, c + 1, k),
                dp(baseline, a, b, c + 2, k - 1) + items[baseline][2] + items[baseline + 1][2],
            )
    if a == b == 0:
        ans = max(ans, dp(baseline, a + 1, b + 1, c, k - 1) + items[baseline][0] + items[baseline][1])
    if b == c == 0:
        ans = max(ans, dp(baseline, a, b + 1, c + 1, k - 1) + items[baseline][1] + items[baseline][2])
    return ans


n, k = cin_int_ls()
items = []
for _ in range(n):
    items.append(cin_int_ls())

ans = dp(0, 0, 0, 0, k)
print(ans)
