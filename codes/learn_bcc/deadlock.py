import threading
import time

lock1 = threading.Lock()
lock2 = threading.Lock()


def run1():
    while True:
        lock1.acquire()
        print("1 Lock 1")
        time.sleep(0.5)
        lock2.acquire()
        lock2.release()
        lock1.release()
        print('running 1')


def run2():
    while True:
        lock2.acquire()
        print("2 Lock 2")
        lock1.acquire()
        lock1.release()
        lock2.release()



t1 = threading.Thread(target=run1)
t2 = threading.Thread(target=run2)

t1.start()
t2.start()


t1.join()
t2.join()