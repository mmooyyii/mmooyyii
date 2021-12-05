import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


def has_card(hand, n):
    return hand & (1 << n) != 0


def set_card(hand, n):
    return hand | (1 << n)


def main():
    memo = {}

    def dp(hand, coins):
        if (hand, coins) in memo:
            return memo[(hand, coins)]
        popcount = bin(hand).count('1')
        if (len(cards) - popcount) * k <= coins:
            return popcount + coins
        base = 0
        for n, p in enumerate(cards):
            if has_card(hand, n):
                base += dp(hand, coins + 1) * p
            else:
                base += dp(set_card(hand, n), coins) * p
        memo[(hand, coins)] = base
        return base

    n, k = cin_int_ls()
    if not (1 <= n <= 5 and 1 <= k <= 5):
        print(0)
        return
    cards = list(map(float, input().split()))
    print(format(dp(0, 0), '.12f'))




"""
16 5
0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.15 0.15 
"""

from itertools import permutations

for i in permutations([2, 2, 8, 8, 2], 3):
    print(list(i))
