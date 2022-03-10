import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


n, k = cin_int_ls()
k -= 1
ls = cin_int_ls()


def check(threshold):
    for i in ls:
        if i > threshold:
            return int(2e9), 0

    a, b = 0, 0
    need = 0
    count = 0
    for i in ls:
        if (a + i) * (b + 1) > threshold:
            count += a * b
            a = i
            b = 1
            need += 1
        else:
            a += i
            b += 1

    count += a * b
    return need, count


# 2分答案， 感觉挺对的
left, right = 1, 1 << 64
while left < right:
    mid = (right + left) // 2
    if check(mid)[0] <= k:
        right = mid
    else:
        left = mid + 1

print(check(left)[1])
