import math


def 调和级数():
    # 1 + 1/2 + 1/3 + 1/4 .... 1/n 大约是 O(log(n))
    for c in [10000, 20000, 30000, 40000, 50000]:
        ans = 0
        for i in range(1, c + 1):
            ans += c // i
        print(int((math.log(c) * c)), ans)


调和级数()
