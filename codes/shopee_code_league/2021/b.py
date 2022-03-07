import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())

# 如果混合后的咖啡浓度大于k, 其中至少有一个咖啡豆的浓度大于等于k
# 整体做法是不断地合并区间
