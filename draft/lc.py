from typing import *

import sys

sys.setrecursionlimit(int(1e9))


class Solution:
    def catMouseGame(self, graph: List[List[int]]) -> int:
        from functools import lru_cache

        @lru_cache(None)
        def dp(maomao, shushu, pos, depth=0):
            if shushu == 0:
                return 1
            if maomao == shushu:
                return 2
            if depth > 200:
                return 0
            if pos == 0:
                tmp = set()
                for nxt in graph[shushu]:
                    if nxt != maomao:
                        v = dp(maomao, nxt, 1 - pos, depth + 1)
                        if v == 1:
                            return 1
                        tmp.add(v)
                if 0 in tmp:
                    ans = 0
                else:
                    ans = 2
            else:
                tmp = set()
                for nxt in graph[maomao]:
                    if nxt != 0:
                        v = dp(nxt, shushu, 1 - pos, depth + 1)
                        if v == 2:
                            return 2
                        tmp.add(v)
                if 0 in tmp:
                    ans = 0
                else:
                    ans = 1
            return ans

        ans = dp(2, 1, 0)
        dp.cache_clear()
        return ans


a = Solution().catMouseGame()
print(a)
