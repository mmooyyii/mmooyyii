from typing import *

import sys

sys.setrecursionlimit(int(2e9))


class Solution:
    def catMouseGame(self, graph: List[List[int]]) -> int:

        memo = {}

        def dp(maomao, shushu, pos, depth=0):
            key = (maomao, shushu, pos)
            if key in memo:
                return memo[key]
            if depth > 1000:
                return 0
            if shushu == 0:
                return 1
            if maomao == shushu:
                return 2
            ans = 0
            if pos == 0:
                tmp = set()
                for nxt in graph[shushu]:
                    tmp.add(dp(maomao, nxt, 1 - pos, depth + 1))
                if 1 in tmp:
                    ans = 1
                elif 0 in tmp:
                    ans = 0
                else:
                    ans = 2
            else:
                tmp = set()
                for nxt in graph[maomao]:
                    if nxt != 0:
                        tmp.add(dp(nxt, shushu, 1 - pos, depth + 1))
                if 2 in tmp:
                    ans = 2
                elif 0 in tmp:
                    ans = 0
                else:
                    ans = 1
            memo[key] = ans
            return ans

        return dp(2, 1, 0)


a = Solution().catMouseGame([[5, 6], [3, 4], [6], [1, 4, 5], [1, 3, 5], [0, 3, 4, 6], [0, 2, 5]])
print(a)
