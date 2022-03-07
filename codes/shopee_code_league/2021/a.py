import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


from functools import lru_cache


@lru_cache(None)
def dp(day, where):
    if day == len(matrix):
        return 0
    if where == 'l':
        return max(
            dp(day + 1, 'l'),  # choice 1 不动
            dp(day + 1, 'l') + matrix[day][0],  # choice 2 从左到右拿水果
            dp(day + 1, 'r'),  # choice 3 去右边
        )
    else:
        return max(
            dp(day + 1, 'r'),  # choice 1 不动
            dp(day + 1, 'r') + matrix[day][1],  # choice 2 从右到左拿水果
            dp(day + 1, 'l'),  # choice 3 去左边
        )


for _ in range(cin_int()):
    n, m = cin_int_ls()
    matrix = []
    for _ in range(n):
        ls = cin_int_ls()
        pre_max1 = 0
        cur = 0
        for i in ls:
            cur += i
            pre_max1 = max(pre_max1, cur)
        pre_max2 = 0
        cur = 0
        for i in ls[::-1]:
            cur += i
            pre_max2 = max(pre_max2, cur)
        matrix.append([pre_max1, pre_max2])
    ans = dp(0, 'l')
    dp.cache_clear()
    print(ans)
