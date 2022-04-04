import os
import time

# 测试数据
gen_test = 'python3 faker.py'
# 目标程序
target = 'python3  cf.py'
# 对拍程序
pai = 'python3 bf.py'

for _ in range(1):
    seed = int(time.time() * 10000)
    start = time.time()
    os.popen(f"{gen_test} {seed} > /tmp/ut.txt").read()
    ans1 = os.popen(f"cat /tmp/ut.txt | {target}").read()
    print("目标程序:", time.time() - start, "秒")
    start = time.time()
    ans2 = os.popen(f"cat /tmp/ut.txt | {pai}").read()
    print("对拍程序", time.time() - start, "秒")
    if ans1 == ans2:
        print("\033[32mACCEPT\033[0m")
    else:
        print("\033[31mWA\033[0m")
        print("输出:")
        print(ans1)
        print("预期:")
        print(ans2)
