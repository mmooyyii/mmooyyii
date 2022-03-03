import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())

# 1. 如果只是单纯的求和,这题怎么做?
# 2. 某节点某方向的边的所有子节点中, 比它大的有几个,深度是多少? 比它小的有几个? 不用管深度的事.
# 3. 
