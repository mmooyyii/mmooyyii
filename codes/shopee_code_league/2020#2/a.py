import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


def climb(ls):
    ans = (0, 0)
    cur = 0
    pre = 0
    for idx, i in enumerate(ls):
        if i == pre + 1:
            pre = i
            cur += 1
        else:
            cur = 0
            pre = 0
        ans = max(ans, (cur, idx))
    if ans == (0, 0):
        return -1, -1
    return ans


for i in range(cin_int()):
    cin_int()
    ls = cin_int_ls()
    a = climb(ls[::-1])
    a = (a[0], len(ls) - a[1] - 1)
    b = climb(ls)
    ans = max(a, b, key=lambda x: (x[0], -x[1]))
    print(f"Case #{i + 1}: {ans[0]} {ans[1]}")
