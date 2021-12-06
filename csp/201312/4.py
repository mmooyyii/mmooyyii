import sys

sys.setrecursionlimit(int(1e9))


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


def make_available():
    ans = {}
    for k in range(0b0000, 0b1111 + 1):
        b = bin(k)[2:].zfill(4)
        tmp = []
        if b[1] == '0' and k != 0:  # 0前不能有1,最高位数字不为0
            tmp.append(0)
        if b[0] == '1':  # 1前一定有0
            tmp.append(1)
        if b[3] == '0':
            tmp.append(2)
        if b[2] == '1':
            tmp.append(3)
        ans[k] = tmp
    return ans


available = make_available()

from functools import lru_cache

mod = int(1e9) + 7


@lru_cache(None)
def dp(n, status):
    if n == 0:
        return 1 if status == 0b1111 else 0
    ava = available[status]
    ans = 0
    for i in ava:
        ans += dp(n - 1, status | (1 << (3 - i)))
    return ans % mod


def force(n):
    ans = 0
    import re
    l, r = 10 ** (n - 1), 10 ** n
    for i in range(l, r):
        i = str(i)
        if set("0123") == set(i):
            if re.findall("3.*?2", i) or re.findall("1.*?0", i):
                pass
            else:
                ans += 1
    return ans


def make_table():
    ans = {}
    for i in range(4, 1001):
        ans[i] = dp(i, 0b0000)
    print(ans)


print(dp(cin_int(), 0b0000))
