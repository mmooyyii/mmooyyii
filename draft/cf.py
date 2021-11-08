import bisect
import random
import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


def fib(n):
    if n <= 2:
        return 1
    return _fib(n - 2, 1, 1)


def _fib(n, a, b):
    if n == 0:
        return a + b
    return _fib(n - 1, b, a + b)
