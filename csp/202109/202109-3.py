# 数组推导
import sys

sys.setrecursionlimit(int(1e9))


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


class MyRand:
    MAXINT64 = (1 << 64) - 1

    def __init__(self):
        self.nxt = 1

    def get(self):
        self.nxt = (self.nxt * 1103515245 + 12345) & MyRand.MAXINT64
        return (self.nxt // 65536) % 32768


class Cell:

    def __init__(self):
        pass


mr = MyRand()


def main():
    n, s, p, t = cin_int_ls()
    dt = cin_int()
    while n != 0:
        rn, v, u, a, b, c, d = cin_int_ls()
        n -= rn
    for _ in range(p):
        r = cin_int()
    for _ in range(s):
        s, t, w, d = cin_int_ls()


# main()
for _ in range(10):
    print(mr.get())
