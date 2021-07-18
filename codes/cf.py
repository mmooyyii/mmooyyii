class KarpRabin:

    def __init__(self, string, n, maxint=1 << 64, big_primes=None):
        if n > len(string):
            raise ValueError
        if big_primes is None:
            self.big_primes = [16777619]
        self.big_primes = big_primes
        self.maxInt = maxint
        self.length = 0
        self.hash = [0 for _ in self.big_primes]
        self.s = string
        self.n = n
        self.to_int = int
        self.sub_memo = {}
        for char in string[:n]:
            self.add_tail(char)

    def add_tail(self, char):
        for i in range(len(self.big_primes)):
            self.hash[i] *= self.big_primes[i]
            self.hash[i] += self.to_int(char)
            self.hash[i] %= self.maxInt
        self.length += 1

    def sub_head(self, char):
        for i in range(len(self.big_primes)):
            sub = pow(self.big_primes[i], self.length - 1, self.maxInt)
            sub *= self.to_int(char)
            sub %= self.maxInt
            self.hash[i] += self.maxInt
            self.hash[i] -= sub
            self.hash[i] %= self.maxInt
        self.length -= 1

    def scan(self):
        yield tuple(self.hash)
        for i in range(len(self.s) - self.n):
            tail = self.s[i + self.n]
            self.add_tail(tail)
            head = self.s[i]
            self.sub_head(head)
            yield tuple(self.hash)


class Solution:
    def longestCommonSubpath(self, n: int, paths) -> int:
        def check(length):
            if length > len(paths[0]):
                return False
            memo = set()
            for i in KarpRabin(paths[0], length,maxint=10 ** 12 + 73,big_primes=n).scan():
                memo.add(i)
            for s in paths[1:]:
                if length > len(s):
                    return False
                tmp = set()
                for i in KarpRabin(s, length).scan():
                    tmp.add(i)
                memo &= tmp
                if len(memo) == 0:
                    return False
            return True

        paths.sort(key=lambda x: len(x))
        left = 0
        right = len(paths[0])

        while left < right:
            mid = (right + left) // 2
            if check(mid):
                left = mid + 1
            else:
                right = mid
        for i in range(left + 2, left - 2, -1):
            if check(i):
                return i


a = Solution().longestCommonSubpath(10, [[2, 1, 4, 0, 3], [2, 1, 4, 0, 3]])
print(a)


class Solution:

    def longestCommonSubpath(self, n: int, paths) -> int:

        def get_set(n, path, p, k):
            s = set()
            cur = 0
            for i in range(k):
                cur *= n
                cur += path[i]
                cur %= p
            s.add(cur)
            for i in range(k, len(path)):
                cur *= n
                cur += path[i]
                cur -= pow(n, k, p) * path[i - k]
                cur %= p
                s.add(cur)
            return s

        def check(n, paths, p, k):
            s = get_set(n, paths[0], p, k)
            print(s)
            for i in range(1, len(paths)):
                t = get_set(n, paths[i], p, k)
                s &= t
                if len(s) == 0:
                    return False
            return True

        p = 10 ** 12 + 73

        left = 0
        right = min([len(path) for path in paths]) + 1
        while left + 1 < right:
            mid = (left + right) // 2
            if check(n, paths, p, mid):
                left = mid
            else:
                right = mid
        return left


a = Solution().longestCommonSubpath(10, [[2, 1, 4, 0, 3], [2, 1, 4, 0, 3]])
print(a)
