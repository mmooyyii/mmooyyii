import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


import bisect


class KDTree:

    def __init__(self, points):
        pass

    def count(self, x, y) -> int:
        pass


people, wifi = [], []
for _ in range(cin_int()):
    people.append(cin_int_ls())
wifi1_x, wifi1_y, wifi2_x, wifi2_y = cin_int_ls()
distance = []
wifi_1 = []
wifi_2 = []
for x, y in people:
    d1 = abs(x - wifi1_x) ** 2 + abs(y - wifi1_y) ** 2
    d2 = abs(x - wifi2_x) ** 2 + abs(y - wifi2_y) ** 2
    distance.append([d1, d2])
    wifi_1.append(d1)
    wifi_2.append(d2)
wifi_1.sort()
wifi_2.sort()
kd_tree = KDTree(distance)
# 1. 如果2个圆没有交集 二分查找,结果相加
# 2. 如果2个圆有交集, 找出交集的点数(树套树, cdq分治)
# 3. 如果1个圆被完全覆盖 二分查找,结果相减
# 其实只有一种情况, 即 wifi1数量 + wifi2数量 - 2 * (重叠区域数量)
for _ in range(cin_int()):
    r1, r2 = cin_int_ls()
    wifi1_cover = bisect.bisect_right(wifi_1, r1 * r1)
    wifi2_cover = bisect.bisect_right(wifi_2, r2 * r2)
    print(wifi1_cover + wifi2_cover - 2 * kd_tree.count(r1 ** 2, r2 ** 2))
