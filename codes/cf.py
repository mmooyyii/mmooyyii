from sys import setrecursionlimit
from typing import *

setrecursionlimit(int(1e9))


class Solution:
    def deleteDuplicateFolder(self, paths: List[List[str]]) -> List[List[str]]:

        t = {}
        for path in paths:
            node = t
            for i in path:
                node = node.setdefault(i, {})

        def dfs(node):
            for k, v in node.items():
                dfs(v)
                v = {'*': v}
                if len(v) == 1 and list(v.values())[0] == {}:
                    pass
                elif v != {}:
                    d = str(v)
                    delete.setdefault(d, 0)
                    delete[d] += 1

        def dfs2(node):
            ddd = []

            for k, v in node.items():
                v = {'*': v}
                if len(v) == 1 and list(v.values())[0] == {}:
                    pass
                elif v != {}:
                    d = str(v)
                    if d in delete and delete[d] >= 2:
                        delete.setdefault(d, 0)
                        ddd.append(k)
            for k, v in node.items():
                dfs2(v)
            for i in ddd:
                node.pop(i)

        delete = {}
        dfs(t)
        dfs2(t)

        def dfs3(node):
            if len(node) == 1 and list(node.values())[0] == {}:
                return [list(node.keys())]
            ret = []
            for k, v in node.items():
                if v == {}:
                    ret.append([k])
                else:
                    for sub in dfs3(v):
                        ret.append([k] + sub)
            return ret

        tmp = dfs3(t)
        ret = set()
        for p in tmp:
            for i in range(1, len(p) + 1):
                ret.add(tuple(p[:i]))
        return sorted([list(i) for i in ret])


a = Solution().deleteDuplicateFolder(
    paths=[["a"], ["a", "x"], ["a", "x", "y"], ["a", "z"], ["b"], ["b", "x"], ["b", "x", "y"], ["b", "z"]])

print(a)
