# 迪菲-赫尔曼密钥交换流程
import random


def eve(func):
    def _func(*args):
        ans = []
        for i in args:
            if type(i) == int:
                ans.append(i)
        print("eve knows", *ans)
        return func(*args)

    return _func


class Peer:

    def __init__(self):
        self.secret = -1
        self.send_number = -1
        self.recv_number = -1

    def send(self, other, number):
        self.send_number = number
        self.solve()
        other.recv(pow(g, number, p))

    @eve
    def recv(self, number):
        self.recv_number = number
        self.solve()

    def solve(self):
        if self.send_number != -1 and self.recv_number != -1:
            self.secret = pow(self.recv_number, self.send_number, p)


p = int(1e9) + 7
g = 1665161446161321

Alice = Peer()
Bob = Peer()

Alice.send(Bob, random.randint(1, 48516168476161986476984))
Bob.send(Alice, random.randint(1, 48516168476161986476984))

print("alice secret is", Alice.secret)
print("bob secret is", Bob.secret)
