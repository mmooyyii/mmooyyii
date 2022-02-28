import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


from functools import lru_cache


@lru_cache(None)
def dp(idx, n, pre, self):  # 前一个和自己有没有被买
    if n <= 0:
        return 0
    if idx == len(prices):
        return int(1e18)
    ans = dp(idx + 1, n, self, False)  # 不买
    if pre and self:
        if idx == len(prices) - 1:
            ans = min(ans, dp(idx + 1, n, True, True))  # 没有下一台服务了
        else:
            ans = min(ans, dp(idx + 1, n - 1, True, True))  # 买了送下一台服务器
    elif pre and not self:
        ans = min(ans, dp(idx + 1, n - 2, True, False) + prices[idx])  # 肯定是选择后一台
    elif not pre and self:
        raise RuntimeError  # 应该不会有这种情况
    elif not pre and not self:
        ans = min(ans, dp(idx + 1, n - 2, True, False) + prices[idx])  # 肯定是选择前一台
    return ans


for _ in range(cin_int()):
    _, n = cin_int_ls()
    prices = cin_int_ls()
    a = dp(0, n, True, False)
    dp.cache_clear()
    print(a)
