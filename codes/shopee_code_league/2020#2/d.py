import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


people, wifi = [], []
for _ in range(cin_int()):
    people.append(cin_int_ls())
wifi1_x, wifi1_y, wifi2_x, wifi2_y = cin_int_ls()
distance = []
for x, y in people:
    d1 = abs(x - wifi1_x) ** 2 + abs(y - wifi1_y) ** 2
    d2 = abs(x - wifi2_x) ** 2 + abs(y - wifi2_y) ** 2
    distance.append([d1, d2])

for _ in range(cin_int()):
    r1, r2 = cin_int_ls()
    # 1. 如果2个圆没有交集 二分查找,结果相加

    # 2. 如果2个圆有交集, 找出交集的点数,然后不会了

    # 3. 如果1个圆被完全覆盖 二分查找,结果相减
