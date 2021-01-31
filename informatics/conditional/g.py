a = input()
b = input()
c = input()
if (a == b) and (a == c) and (b == c):
    print(3)
elif (a == b) or (a == c) or (b == c):
    print(2)
else:
    print(0) 