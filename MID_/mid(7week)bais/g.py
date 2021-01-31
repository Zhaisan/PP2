n = int(input())
a = []
for i in range(n):
    x = (input())
    a.append(list(x))
s = set(a[0])
for i in a:
    s = s.intersection(i)
if len(list(s)) > 0:
    for i in sorted(list(s)):
        print(i, end='')
else:
    print('NO COMMON CHARACTERS')