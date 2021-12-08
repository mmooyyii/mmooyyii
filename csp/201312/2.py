isbn = input()
a, b, c, d = isbn.split('-')
su = 0
for i, v in enumerate(a + b + c):
    su += int(v) * (i + 1)

checkSum = su % 11
if checkSum == 10:
    checkSum = 'X'
else:
    checkSum = str(checkSum)

if checkSum == d:
    print("Right")
else:
    print("-".join([a, b, c, checkSum]))
