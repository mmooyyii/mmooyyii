def add(a: str, b: str) -> str:
    a = '0' * (len(b) - len(a)) + a
    b = '0' * (len(a) - len(b)) + b
    add_one = 0
    ret = []
    for i in range(len(a) - 1, -1, -1):
        n = int(a[i]) + int(b[i]) + add_one
        add_one = n // 10
        ret.append(str(n % 10))
    if add_one:
        ret.append(str(add_one))
    ret.reverse()
    return ''.join(ret)


def primary_school(a: str, b: str) -> str:
    ret = '0'
    a = int(a)
    for bit, v in enumerate(b[::-1]):
        ret = add(ret, str(a * int(v) * 10 ** bit))
    return ret


def karatsuba(num1, num2):
    num1Str, num2Str = str(num1), str(num2)

    if num1 < 10 or num2 < 10: return num1 * num2

    maxLength = max(len(num1Str), len(num2Str))
    num1Str = ''.join(list('0' * maxLength)[:-len(num1Str)] + list(num1Str))
    num2Str = ''.join(list('0' * maxLength)[:-len(num2Str)] + list(num2Str))

    splitPosition = maxLength // 2
    high1, low1 = int(num1Str[:-splitPosition]), int(num1Str[-splitPosition:])
    high2, low2 = int(num2Str[:-splitPosition]), int(num2Str[-splitPosition:])
    z0, z2 = karatsuba(low1, low2), karatsuba(high1, high2)
    z1 = karatsuba((low1 + high1), (low2 + high2))
    return z2 * 10 ** (2 * splitPosition) + (z1 - z2 - z0) * 10 ** (splitPosition) + z0


def toom_cook(a, b):
    pass


a = '35809182308109238019248091274907120471209381920830917429012938'
b = '111375918209471920574102947091725109237912489712984618926591825691821'
c = str(int(a) * int(b))
c1 = primary_school(a, b)
c2 = karatsuba(int(a), int(b))
print(c)
print(c1)
print(c2)
