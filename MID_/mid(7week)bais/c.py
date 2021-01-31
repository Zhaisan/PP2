n=int(input())
ar=[int(i) for i in input().split()]
ar=set(ar)
ind=0
for u in sorted(ar):
    print(ind+1,u)
    ind+=1