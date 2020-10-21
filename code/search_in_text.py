import random
import time
import re

alpha = 'qwertyuiop1234567890asdfghjklzxcvbnmQWERTYUIOPASDFGHJKZXCVBNM         '

code = ''.join([random.choice(alpha) for _ in range(5_000)])


class InvertedIndex:

    def __init__(self, text):
        self.origin_text = text
        self.window_size = 4
        self.index = self.build_index(text)

    def build_index(self, text):
        ret = {}
        for window_size in range(1, self.window_size + 1):
            for index in range(len(text) - window_size + 1):
                window = text[index:index + window_size]
                ret.setdefault(window, []).append(index)
        return ret

    def search(self, word):
        if len(word) <= self.window_size:
            return list(map(lambda x: [x, x + len(word)], self.index.setdefault(word, [])))
        else:
            ret = []
            for index in range(len(word) - self.window_size + 1):
                sub_text = word[index:index + self.window_size]
                possibles = self.index.setdefault(sub_text, [])
                for possible in possibles:
                    left = possible - index
                    right = left + len(word)
                    if self.origin_text[left:right] == word:
                        ret.append((left, right))
            return ret


start = time.time()
i = InvertedIndex(code)
for _ in range(50000):  # 36.39s
    pattern = ''.join([random.choice(alpha) for _ in range(4)])
    i.search(pattern)
print(time.time() - start)
start = time.time()
for _ in range(50000):  # 125.61s
    pattern = ''.join([random.choice(alpha) for _ in range(4)])
    a = pattern in code
print(time.time() - start)
