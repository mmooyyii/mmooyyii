import bisect
import random
import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


def slow(n):
    ans = 0
    for i in range(1, n + 1):
        ans += n // i
    return ans


def quick(n):
    ans = 0
    l, r = 1, 0
    while l <= n:
        r = n // (n // l)
        ans += (r - l + 1) * (n // l)
        l = r + 1
    return ans


b = quick(7772)
print(b)
