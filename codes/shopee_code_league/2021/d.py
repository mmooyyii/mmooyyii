import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


n, k = cin_int_ls()
ls = cin_int_ls()


def check(threshold):
    a, b = 1, 1
    need = 0
    for i in ls:
        if (a + i) * (b + 1) > threshold:
            a = i
            b = 1
            need += 1
        else:
            a += i
            b += 1
    return need <= k

# 2分答案， 感觉挺对的
left, right = 0, 1 << 64
while left < right:
    mid = (right + left) // 2
    if check(mid):
        right = mid
    else:
        left = mid + 1

print(left * k)
