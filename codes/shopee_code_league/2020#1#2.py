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


def solve2():
    # 下面写法时间复杂度是O(121 * N), 空间复杂度O(121 * N).
    # 用字符串哈希时间复杂度可以到O(11 * N), 空间复杂度有点难算, 应该比O(121 * N)小.
    from collections import defaultdict
    for _ in range(cin_int()):
        n, q = cin_int_ls()
        invert_index = defaultdict(set)
        for i in range(n):
            item = input().split()
            # 这里用字符串哈希可以到O(11 * n)
            for l in range(0, len(item)):
                for r in range(l + 1, len(item) + 1):
                    invert_index[tuple(item[l:r])].add(i)
        for _ in range(q):
            ans = invert_index[tuple(input().split())]
            print(len(ans))


solve1()
solve2()
