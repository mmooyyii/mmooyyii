import json
import sys


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())




import xmltodict

with open(r"D:\workdir\articleServer\http\jmeter\TestPlan.jmx", 'r', encoding='utf8') as f:
    j = json.dumps(xmltodict.parse(f.read()), indent=4, ensure_ascii=False)
    print(j)

print(xmltodict.unparse(j))


