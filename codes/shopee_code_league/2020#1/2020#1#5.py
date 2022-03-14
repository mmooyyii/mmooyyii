import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


from collections import Counter
import math
n, m, k = cin_int_ls()
num = Counter()
# 把所有的结果算出来,对k取模后存起来, 这里可以O(n)
for i in range(1, n + 1):
    a, b, c = cin_int_ls()
    for j in range(1, c + 1):
        print(i, j, (a * j + b))
        num[(a * j + b) % k] += 1
print(num)

# m很大,肯定需要快速幂,但是这也太大了吧
print(2000 ** math.log2(7) * math.log2(int(1e9)))