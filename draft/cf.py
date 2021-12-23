import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


from functools import lru_cache


def make_plan(n):
    plan = []
    for a in range(101):
        for b in range(101):
            for c in range(101):
                if (a + b + b + c + c + c) == n:
                    plan.append([a, b, c])

    return plan


plan = make_plan(7)
for i in range(2, 3):
    p = make_plan(i * 7)
    tmp = []
    for a, b, c in p:
        for aa, bb, cc in plan:
            if a >= aa and b >= bb and c >= cc:
                break
        else:
            tmp.append([a, b, c])
    plan.extend(tmp)
for a, b, c in plan:
    print(f"{{{a},{b},{c}}},")


# @lru_cache(None)
# def dp(one, two, three):
#     ans = 0
#     for a, b, c in plan:
#         if one >= a and two >= b and three >= c:
#             ans = max(ans, dp(one - a, two - b, three - c) + 1)
#     return ans
#
#
# import time
#
# start = time.time()
# for _ in range(cin_int()):
#     cin_int()
#     print(dp(*cin_int_ls()))
