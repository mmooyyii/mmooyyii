import os
import time

# 测试数据
gen_test = 'python3 faker.py'
# 目标程序
target = 'python3 cf.py'
# 判定程序
judge = 'python3 judgemt.py'


def accept():
    print("\033[32mACCEPT\033[0m")

def wa():
    print("\033[31mWA\033[0m")

for _ in range(10):
    os.popen(f"{gen_test} > /tmp/ut.txt").read()
    start = time.time()
    os.popen(f"cat /tmp/ut.txt | {target} > /tmp/out.txt").read()
    print("运行时间:", time.time() - start, "秒")
    ans = os.popen(f"cat /tmp/ut.txt /tmp/out.txt | {judge}").read()
    start = time.time()
    if "YES" in ans:
        accept()
    else:
        wa()
        print("输出:")
        os.system("cat /tmp/out.txt")
        print(ans)
