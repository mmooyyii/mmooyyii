"""
数据库常用的4种事务隔离级别的简单实现
"""

"""
shared lock：   
查询中的每行都加共享锁，
当没有其他线程对查询结果集中的任何一行使用排他锁时，
可以成功申请共享锁，否则会被阻塞。

exclusive lock： 同threading.Lock()
"""

"""
先简单地写个数据库
"""
import time
import threading
import random
import uuid


class SharedLock:

    def __init__(self):
        self.writeLock = threading.Lock()
        self.thread_id = None

    def acquire(self, thread_id):
        self.writeLock.acquire()
        self.thread_id = thread_id

    def release(self, thread_id):
        if self.thread_id == thread_id:
            self.writeLock.release()
        else:
            raise RuntimeError

    def shared(self):
        if not self.thread_id:
            return
        else:
            self.writeLock.acquire()
            self.writeLock.release()


class Table:

    def __init__(self):
        self.data = {}
        self.readLocks = {}
        self.writeLocks = {}

    def read(self, k):
        return self.data[k]

    def write(self, k, v):
        if k not in self.data:
            self.readLocks[k] = SharedLock()
            self.writeLocks[k] = threading.Lock()
        self.data[k] = v

    def get_read_lock(self, k) -> threading.Lock:
        self.readLocks[k].shared()
        return self.readLocks[k]

    def get_write_lock(self, k) -> threading.Lock:
        return self.writeLocks[k]


"""
1. Serialization
"""

"""
# 1) 2PL（two-phase locking） 2阶段锁定
如果一个transaction想要读取x ，那它必须获取x的shared lock；
如果一个transaction想要写入x ，那它必须获取x上的exclusive lock。
如果一个transaction释放了它所持有的任意一个锁，那它就再也不能获取任何锁。
"""

# 不可重复读（Non Repeatable Read）的问题
# a和b都有100块钱，2者间会产生随机的交易，任何时候查询2者的总和都是200
t = Table()
c = ['a', 'b']
a, b = c
t.write(a, 100)
t.write(b, 100)


def r():
    for _ in range(10000):
        time.sleep(0.01)
        t.get_read_lock(a)
        t.get_read_lock(b)
        v1 = t.read(a)
        v2 = t.read(b)
        print('count', v1 + v2)
        v1 = t.read(a)
        v2 = t.read(b)
        print('count', v1 + v2)
        v1 = t.read(a)
        v2 = t.read(b)
        print('count', v1 + v2)
        v1 = t.read(a)
        v2 = t.read(b)
        print('count', v1 + v2)


def f():
    th_id = str(uuid.uuid1())
    for _ in range(100000):
        # begin
        random.shuffle(c)
        a, b = c
        shared_locks = []
        n = random.randint(10, 20)
        shared_locks.append(t.get_read_lock(a))
        v1 = t.read(a)
        shared_locks.append(t.get_read_lock(b))
        v2 = t.read(b)
        ela = t.get_write_lock(a)
        ela.acquire()
        for lock in shared_locks:
            lock.acquire(th_id)
        t.write(a, v1 + n)
        elb = t.get_write_lock(b)
        elb.acquire()
        t.write(b, v2 - n)
        # 开始释放锁
        ela.release()
        elb.release()
        for lock in shared_locks:
            lock.release(th_id)
        # commit


threading.Thread(target=r).start()
for _ in range(100):
    th = threading.Thread(target=f)
    th.start()
    th.join()

"""
2. Repeatable Read
"""

"""
3. Read Committed
"""

"""
4. Read Uncommitted
"""
t = Table()
c = ['a', 'b']
a, b = c
t.write(a, 100)
t.write(b, 100)
# begin
random.shuffle(c)
a, b = c
shared_locks = []
n = random.randint(10, 20)
v1 = t.read(a)
v2 = t.read(b)

ela = t.get_write_lock(a)
ela.acquire()
t.write(a, v1 + n)
ela.release()

elb = t.get_write_lock(b)
elb.acquire()
t.write(b, v2 - n)
# 开始释放锁
elb.release()
# commit
