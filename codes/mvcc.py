from typing import *


class Solution:
    def electricityExperiment(self, row: int, col: int, position: List[List[int]]) -> int:
        def calc(x1, y1, x2, y2):
            dx, dy = abs(x1 - x2), abs(y1 - y2)
            if dy < dx:
                return 0
            layers = [1]
            l, r = x1, x1 + 1
            for _ in range(dy):
                l, r = l - 1, r + 1
                if l < 0:
                    l = 0
                if r >= row:
                    pass
                nxt_layer = [0] * (r - l)
                offset = 1
                for i in range(len(nxt_layer)):
                    v = 0
                    for idx in (i - offset - 1, i - offset, i - offset + 1):
                        if 0 <= idx < len(layers):
                            v += layers[idx]
                    nxt_layer[i] = v
                layers = nxt_layer
            return layers

        a = calc(1, 1, 4, 4)
        print(a)
        # position.sort(key=lambda x: x[1])
        # ans = 1
        # x, y = position[0]
        # for nx, ny in position[1:]:
        #     ans *= calc(x, y, nx, ny)
        #     ans %= (int(1e9) + 7)
        #     x, y = nx, ny
        # return ans


Solution().electricityExperiment(row=5, col=6, position=[[1, 3], [3, 5], [2, 0]])
