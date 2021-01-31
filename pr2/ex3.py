l = list(map(int,input().split()))
i = int(input())
def f(lis, ind):
    l = []
    for i in range(0,ind):
        l.append(lis[i])
    for i in range(ind,len(lis)):
        a = lis[i]*lis[i]
        l.append(a)
    return l

print(f(l, i))