"""
带混牌的麻将向听数判断和bot
混牌：就是万能牌，能当作任意牌使用,
本例中，用一张额外的牌作为混牌。
混牌与任意牌的距离都是无限大。
一张混牌能使向听数 - 1
"""

import random
from collections import Counter

万 = list(range(11, 20))
条 = list(range(31, 40))
筒 = list(range(51, 60))
字 = list(range(70, 140, 10))
混 = [1234, 1244, 1254, 1264]

中文牌 = {
    1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九',
    70: '东', 80: '南', 90: '西', 100: '北', 110: '中', 120: '发', 130: '白',
    1234: '混', 1244: '混', 1254: '混', 1264: '混'
}


class Pai:

    def __init__(self):
        self.pais = (万 + 条 + 筒 + 字) * 4 + 混
        random.shuffle(self.pais)
        self.index = 0

    def 发牌(self):
        self.index += 13
        return self.pais[:self.index]

    def 摸(self):
        self.index += 1
        return self.pais[self.index]


def ting(pai):
    pai.append(999)  # 原算法只适用于 2，5，8，11，14张牌的情况，加一张无用牌适配成能检测13张牌的情况
    return _ting(pai)


def _ting(pai: list, K=0, P=0, G=0, g=0, step=0):  # 13张
    count = Counter(pai)
    if step == 0:  # 确定K
        K = (len(pai) - 2) // 3
        return _ting(pai, K, P, G, g, step + 1)
    elif step == 1:  # 取雀头,如果有设P=1
        ret = []
        for k, v in count.items():
            if v >= 2:
                p = pai[:]
                p.remove(k), p.remove(k)
                ret.append(_ting(p, K, 1, G, g, step + 1))
        ret.append(_ting(pai[:], K, 0, G, g, step + 1))
        return min(ret)
    elif step == 2:  # 取完整的顺刻
        shun = get_shun(count)
        ke = get_ke(count)
        if shun:
            for p in shun:
                pai.remove(p)
            return _ting(pai, K, P, G + 1, g, step)
        elif ke:
            for p in ke:
                pai.remove(p)
            return _ting(pai, K, P, G + 1, g, step)
        else:
            return _ting(pai, K, P, G, g, step + 1)
    elif step == 3:  # 取缺一张的顺刻
        shun = get_half_shun(count)
        ke = get_half_ke(count)
        if shun:
            for p in shun:
                pai.remove(p)
            return _ting(pai, K, P, G, g + 1, step)
        elif ke:
            for p in ke:
                pai.remove(p)
            return _ting(pai, K, P, G, g + 1, step)
        else:
            return _ting(pai, K, P, G, g, step + 1)
    elif step == 4:  # 计算S值
        hun = get_hun_number(count)
        if g == 2 + hun and P == 0:
            return 2 * (K - G) - g - P + 1 - hun
        else:
            return 2 * (K - G) - g - P - hun


def get_shun(count):
    for k, v in count.items():
        if k + 1 in count and k + 2 in count:
            return [k, k + 1, k + 2]


def get_ke(count):
    for k, v in count.items():
        if v >= 3:
            return [k, k, k]


def get_half_shun(count):
    for k, v in count.items():
        if k + 1 in count:
            return [k, k + 1]
        elif k + 2 in count:
            return [k, k + 2]


def get_half_ke(count):
    for k, v in count.items():
        if v >= 2:
            return [k, k]


def get_hun_number(count):
    ret = 0
    for p in 混:
        ret += count.setdefault(p, 0)
    return ret


def bot_play(pai):
    # 进14张
    pai.sort()
    mi = float('inf')
    ret = []
    for i in range(len(pai)):
        n = ting(pai[:i] + pai[i + 1:])
        if mi > n:
            mi = n
            ret = [pai[i]]
        elif mi == n:
            ret.append(pai[i])
    play = random.choice(ret)
    if mi == 0:
        pp = pai[:]
        pp.remove(play)
        print(f"听牌！{list(map(to_chinese, pp))}")
        return None
    return play


def to_chinese(pai):
    if 10 <= pai <= 19:
        return f"{中文牌[pai % 10]}万"
    elif 30 <= pai <= 39:
        return f"{中文牌[pai % 10]}条"
    elif 50 <= pai <= 59:
        return f"{中文牌[pai % 10]}筒"
    else:
        return f"{中文牌[pai]}"


if __name__ == '__main__':
    p = Pai()
    pai = p.发牌()
    xun = 0
    while True:
        xun += 1
        m = p.摸()
        print(f'牌: {list(map(to_chinese, pai))} ')
        pai.append(m)
        print(f"摸到 {to_chinese(m)} ")
        play = bot_play(pai)
        if not play:
            print(f"{xun}巡听牌")
            exit(0)
        print(f"打出 {to_chinese(play)} ")
        pai.remove(play)
