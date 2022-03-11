import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


from collections import Counter

n, m, k = cin_int_ls()
num = Counter()
for i in range(n):  # 这里可以O(n)
    a, b, c = cin_int_ls()
    for j in range(1, c + 1):
        num[(a * j + b) % k] += 1


def comb_plan(k, m, have):
    # 需要特判0的情况
    ls = list(have)
    ls.sort(reverse=True)
    # 把k切分成几种组合方案
    todo = [[k, []]]
    for i in ls:
        new = []
        for rest, plan in todo:
            ma = m - len(plan)
            for cut in range(min((rest // i) + 1, ma + 1)):
                p = plan.copy()
                p.extend([i] * cut)
                new.append([rest - cut * i, p])
        todo = new
    ans = []
    for i, plan in todo:
        if i == 0:
            ans.append(plan)
    return ans


print(comb_plan(2000, 3, list(range(1, 2000))))
