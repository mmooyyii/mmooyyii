import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


# 如果混合后的咖啡浓度大于k, 其中至少有一个咖啡豆的浓度大于等于k
# 整体做法是不断地合并区间

import fractions

n, k = cin_int_ls()
coffee_bean = cin_int_ls()
ans = 0
start = []
for i, v in enumerate(coffee_bean):
    if v >= k:
        ans += 1
        if start and start[-1][-1] == i:
            ans += (start[-1][-1] - start[-1][0])
            start[-1][-1] = i + 1
        else:
            start.append([i, i + 1])

print(start, ans)
while start:
    l, r = start.pop()

