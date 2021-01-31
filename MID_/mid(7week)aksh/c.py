n = int(input())
a = [int(i) for i in input().split()]
s = set(a)
if len(a)==len(s):
    print("YES")
else:
    print("NO")
