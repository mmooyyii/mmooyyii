import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


# 1 ≤ N ≤ 104
# 1 ≤ Q ≤ 104
# 字符总长度 < 7 * 105
# 看其他题的排版是正常的,应该就是这个数据量吧????
# 但是是不是太过简单了?

def solve1():
    for _ in range(cin_int()):
        n, q = cin_int_ls()
        items = []
        for _ in range(n):
            items.append(" " + input() + " ")
        for _ in range(q):
            pattern = " " + input() + " "
            ans = 0
            for i in items:
                if pattern in i:
                    ans += 1
            print(ans)


class KarpRabin:
    big_primes = [16777619]
    maxInt = 1 << 32
    to_int = ord

    def __init__(self):
        from collections import deque
        self.hash = [0 for _ in KarpRabin.big_primes]
        self.string = deque()

    def append(self, char):
        for i in range(len(KarpRabin.big_primes)):
            self.hash[i] = ((self.hash[i] * KarpRabin.big_primes[i]) + KarpRabin.to_int(char)) % KarpRabin.maxInt
        self.string.append(char)
        return self

    def extend(self, string):
        for char in string:
            self.append(char)
        return self

    def popleft(self):
        char = self.string.popleft()
        for i in range(len(KarpRabin.big_primes)):
            self.hash[i] -= pow(KarpRabin.big_primes[i], len(self.string), KarpRabin.maxInt) * KarpRabin.to_int(char)
            self.hash[i] %= KarpRabin.maxInt
        return self

    def hash_value(self):
        return tuple(self.hash)

    def to_string(self):
        return ''.join(list(self.string))


def solve2():
    # N是总字符数
    # 时间复杂度O(11 * N)
    # 空间复杂度: 最坏情况下,每个商品名10个空格,单词的长度是4或5,而且每个都不同,最多14000个商品, 需要14000 * 121个int
    from collections import Counter
    for _ in range(cin_int()):
        n, q = cin_int_ls()
        invert_index = Counter()
        for i in range(n):
            item = input().split()
            tmp = set()
            for l in range(0, len(item)):
                k = KarpRabin()
                for r in range(l, len(item)):
                    k.extend(item[r])
                    tmp.add(k.hash_value())
                    k.append(' ')
            for h in tmp:
                invert_index[h] += 1
        for _ in range(q):
            ans = invert_index[KarpRabin().extend(input()).hash_value()]
            print(ans)


# solve1()
solve2()
