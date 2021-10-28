import os
import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


def talk(text):
    print(text)
    sys.stdout.flush()


if __name__ == '__main__':
    pass
