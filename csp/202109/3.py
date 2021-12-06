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

    def __init__(self, a, b, c, d, dt):
        self.a, self.b, self.c, self.d = a, b, c, d
        self.vk_1 = 0
        self.uk_1 = 0
        self.dt = 0
        self.ik = 0

    def nxt(self, shock):
        vk_1, uk_1 = self.vk_1, self.uk_1

        new_vk = vk_1 + self.dt * (0.04 * vk_1 * vk_1 + 5 * vk_1 + 140 - uk_1) + self.ik
        new_uk = uk_1 + self.dt * self.a * (self.b * vk_1 - uk_1)


        self.vk_1, self.uk_1 = new_vk, new_uk
        return


mr = MyRand()

c = Cell(0.02, 0.2, -65.0, 2.0, 0.1)
print(c.nxt())


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
    for _ in range(t):
        pass



for _ in range(10):
    print(mr.get())
