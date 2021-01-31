def average():
    av = (a[0]+a[1]+a[2])/3
    return av


n , x = input().split()
i = 0 
while i < int(n):
    i +=1
    a = [int(i) for i in input().split()]
    if average()>=int(x):
        print("YES")
        exit()
print("NO")
