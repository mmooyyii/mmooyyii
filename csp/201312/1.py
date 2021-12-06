import sys

sys.setrecursionlimit(int(1e9))


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


def main():
    cin_int()
    ls = cin_int_ls()
    from collections import Counter
    c = Counter(ls)
    ma = max(c.values())
    ans = int(1e9)
    for k, v in c.items():
        if v == ma:
            ans = min(ans, k)
    print(ans)


main()
