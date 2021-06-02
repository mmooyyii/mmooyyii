# etcd的mvcc简单实现

import threading

lock = threading.Lock()
global_tid = [0]


class Revision:

    def __init__(self):
        lock.acquire()
        self.main = global_tid[0]
        global_tid[0] += 1
        lock.release()
        self.sub = 0

    def edit(self):
        pass


db = {}
