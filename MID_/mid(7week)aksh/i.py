n = int(input())
a = [int(i) for i in input().split()]
k = int(input())
x = a[0]
y = a[k]
for i in range(0,k - 1):
    x = x * 10 + a[i + 1]

for i in range(k, len(a) - 1):
    y = y * 10 + a[i + 1]

print(x * y)
