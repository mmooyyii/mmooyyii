import bisect
import random
import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


def sv(points, m):
    pass


import socket


def d(func):
    def _warp(*args, **kwargs):
        print(*args, **kwargs)
        return func(*args, **kwargs)

    return _warp


@d
def fun(a):
    pass


fun("123")
