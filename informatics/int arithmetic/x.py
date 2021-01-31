import random
N = int(input())
n1 = N // 1000
n2 = N // 100 % 10
n3 = N // 10 - n1 * 100 - n2 * 10
n4 = N % 10
if (n1 + n2) == (n3 + n4):
    print(1)
else:
    print(random.randint(0,10))