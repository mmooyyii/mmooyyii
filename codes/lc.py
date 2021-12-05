from typing import *

from collections import defaultdict
import json
import time

time_start = time.time()


# Definition for a binary tree node.
class Solution:
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
        if len(pairs) == 1:
            return pairs
        from collections import defaultdict
        s, e = defaultdict(list), defaultdict(list)
        for i, v in enumerate(pairs):
            start, end = v
            s[start].append(i)
            e[end].append(i)

        head = set()
        tail = set()
        for start, end in pairs:
            if len(s[start]) > len(e[start]):
                head.add(start)
            if len(s[end]) < len(e[end]):
                tail.add(end)
        if not head and not tail:
            head = pairs[0][0]
            tail = pairs[1][1]
        elif len(head) > len(tail):
            tail = tail.pop()
            if tail in head:
                head.remove(tail)
            head = head.pop()
        elif len(head) < len(tail):
            head = head.pop()
            if head in tail:
                tail.remove(head)
            tail = tail.pop()
        else:
            head = head.pop()
            if head in tail:
                tail.remove(head)
            tail = tail.pop()
        print(time.time() - time_start)
        weight = [0 for _ in pairs]
        from collections import deque
        q = deque()
        vis = set()
        vis2 = set()
        for idx in e[tail]:
            q.append(idx)
            vis.add(idx)
        print(time.time() - time_start)
        while len(q) != 0:
            idx = q.popleft()
            w = weight[idx]
            start, end = pairs[idx]
            if start not in vis2:
                vis2.add(start)
                for idx in e[start]:
                    if idx not in vis:
                        vis.add(idx)
                        q.append(idx)
                        weight[idx] = w - 1
        print(time.time() - time_start)
        for start, nxt in s.items():
            nxt.sort(key=lambda idx: -weight[idx])
        print(time.time() - time_start)
        ans = []
        while len(ans) != len(pairs):
            start, end = pairs[s[head].pop()]
            ans.append([start, end])
            head = end
        return ans


with open('a.txt', 'r') as f:
    import json

    a = json.load(f)

Solution().validArrangement(a)
print(time.time() - time_start)
