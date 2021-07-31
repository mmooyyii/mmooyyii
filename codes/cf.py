import sys

input = sys.stdin.buffer.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    l = max(0, n - 2 * k - 1)
    ans = -1e12
    for i in range(l, n):
        for j in range(i + 1, n):
            ans = max(ans, (i + 1) * (j + 1) - k * (a[i] | a[j]))
    print(ans)
