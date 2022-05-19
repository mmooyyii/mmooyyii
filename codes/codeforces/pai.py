import os
import time
from subprocess import Popen, PIPE

# 测试数据
gen_test = ['python3', 'faker.py']
# 目标程序
target = ['python3', 'cf.py']
# 对拍程序
pai = ['python3', 'bf.py']

for _ in range(10000):
    start = time.time()
    test_case = Popen(gen_test, stdout=PIPE).stdout.read().decode()
    ans1 = Popen(target, stdout=PIPE, stdin=PIPE)
    ans1 = ans1.communicate(test_case.encode())[0].decode()
    print("目标程序:", time.time() - start, "秒")
    start = time.time()
    ans2 = Popen(pai, stdout=PIPE, stdin=PIPE)
    ans2 = ans2.communicate(test_case.encode())[0].decode()
    print("对拍程序", time.time() - start, "秒")
    if ans1 == ans2:
        print("\033[32mACCEPT\033[0m")
    else:
        print("\033[31mWA\033[0m")
        print("测试用例:")
        print(test_case, end='')
        print("输出:")
        print(ans1, end='')
        print("预期:")
        print(ans2, end='')
        break
