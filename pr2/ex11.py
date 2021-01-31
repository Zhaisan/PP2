def diff(a, b):
    print(a-b)

a = int(input())
aset = {int(input()) for i in range(a)}
b = int(input())
bset = {int(input()) for i in range(b)}
diff(aset, bset)