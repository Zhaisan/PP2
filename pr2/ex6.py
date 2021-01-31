l1 = list(map(int,input().split()))
l2 = list(map(int,input().split()))
i1 = int(input())
i2 = int(input())

def f(l1,l2,i1,i2):
    lis=[]
    for i in range(0,i1):
        lis.append(l1[i])
    for i in range(0,len(l2)):
        lis.append(l2[i])
    for i in range(i1,len(l1)):
        lis.append(l1[i])
    for i in range(i2,len(lis)):
        lis.pop()
    return lis

print(f(l1,l2,i1,i2))