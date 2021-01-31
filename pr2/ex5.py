l = list(map(int,input().split()))
i = int(input())
def f(l, ind):
    for ind in range(ind,len(l)):
        l.pop()
    return l        

print(f(l, i))