def rank(ls):
    rk = [0 for _ in ls]
    ls = [(v, i) for i, v in enumerate(ls)]
    ls.sort()
    pre = 0
    for i in range(len(ls)):
        r = i + 1
        if ls[i - 1][0] == ls[i][0]:
            r = pre
        idx = ls[i][1]
        rk[idx] = r
        pre = r
    return rk


def suffix_array(s):
    rk = rank(s)
    skip = 1
    while skip < len(s):
        source = [[-1, -1] for _ in s]
        for i in range(len(s)):
            source[i][0] = rk[i]
            if i + skip < len(s):
                source[i][1] = rk[i + skip]
        rk = rank(source)
        skip *= 2
    sa = [0 for _ in s]
    for i in range(len(s)):
        sa[rk[i] - 1] = i
    return sa, [i - 1 for i in rk]


def height(s, sa, rk):
    ht = [0] * len(sa)
    k = 0
    for sai in range(0, len(s)):
        if k:
            k -= 1
        while True:
            ai, bi = sai + k, sa[rk[sai] - 1] + k
            if max(ai, bi) >= len(s):
                break
            elif s[ai] == s[bi]:
                k += 1
            else:
                break
        ht[rk[sai]] = k
    return ht


import time

T = "zxcvdqkfawuytt"
start = time.time()
sa, rk = suffix_array(T)
print(time.time() - start)
ht = height(T, sa, rk)
i = ht.index(max(ht))
v = ht[i]
print(sa, rk)
print(ht)
print(T[sa[i]:sa[i] + v])
print(time.time() - start)
