from typing import *
import random


def func(a, n, m):
    if n == 0:
        return 1
    num = func(a, n // 2, m)
    if n % 2 == 0:
        return num * num % m
    else:
        return num * num * a % m


print(func(5, 6, 7))
