n = int(input())
max = 0

a =[int(i) for i in input().split()]
for i in range(len(a)):

    if a[i]>max:
        max = a[i]
        k = i
print(k)




