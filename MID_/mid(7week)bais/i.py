n = int(input())
a = [int(i) for i in input().split()]
b = tuple(a)
b = sorted(b)
if b==a:
    print("Interesting")
else:
    print("Not interesting")
