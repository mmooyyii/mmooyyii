import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


import bisect
from sortedcontainers import SortedList

people, wifi = [], []
for _ in range(cin_int()):
    people.append(cin_int_ls())
wifi1_x, wifi1_y, wifi2_x, wifi2_y = cin_int_ls()
points = []
wifi_1 = []
wifi_2 = []
for x, y in people:
    d1 = abs(x - wifi1_x) ** 2 + abs(y - wifi1_y) ** 2
    d2 = abs(x - wifi2_x) ** 2 + abs(y - wifi2_y) ** 2
    points.append([d1, d2])
    wifi_1.append(d1)
    wifi_2.append(d2)
wifi_1.sort()
wifi_2.sort()

# 1. 如果2个圆没有交集 二分查找,结果相加
# 2. 如果2个圆有交集, 找出交集的点数(树套树, cdq分治, KD树, 离线查询) https://www.luogu.com.cn/problem/P3810
# 3. 如果1个圆被完全覆盖 二分查找,结果相减
# 其实只有一种情况, 即 wifi1数量 + wifi2数量 - 2 * 重叠区域数量
question = []
answer = {}
for _ in range(cin_int()):
    r1, r2 = cin_int_ls()
    question.append([r1, r2])

oq = sorted(question)
points.sort()
points_idx = 0
sl = SortedList()
for r1, r2 in oq:
    while points_idx < len(points) and r1 ** 2 >= points[points_idx][0]:
        sl.add(points[points_idx][1])
        points_idx += 1
    wifi1_cover = bisect.bisect_right(wifi_1, r1 * r1)
    wifi2_cover = bisect.bisect_right(wifi_2, r2 * r2)
    dup = sl.bisect_right(r2 ** 2)
    answer[(r1, r2)] = len(people) - (wifi1_cover + wifi2_cover - 2 * dup)

for r1, r2 in question:
    print(answer[(r1, r2)])
