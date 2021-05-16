import random
import time

with open('../data/莎士比亚全集英文版.txt', 'r') as f:
    code = str(f.read())


def split_by_char(chars, text):
    tmp = []
    for i, char in enumerate(text):
        if char in chars:
            if tmp:
                yield i - len(tmp), ''.join(tmp)
                tmp = []
        else:
            tmp.append(char)
    if tmp:
        yield len(text) - len(tmp), ''.join(tmp)


class InvertedIndex:

    def __init__(self, text):
        self.index = self.build_index(text)

    @staticmethod
    def build_index(text: str):
        d = {}
        for idx, word in split_by_char({'\n', '.', ';', '?', '\t', ' ', ',', '', '!'}, text):
            d.setdefault(word, [])
            d[word].append(idx)

    def search(self, word):
        if word in self.index:
            return self.index[word]
        return []


start = time.time()
i = InvertedIndex(code)
a = i.search("The")
print(a)
# for _ in range(50000):  # 36.39s
#     pattern = 'remainder'
#     i.search(pattern)
# print(time.time() - start)
# start = time.time()
# for _ in range(50000):  # 125.61s
#     pattern = 'remainder'
#     a = pattern in code
print(time.time() - start)
