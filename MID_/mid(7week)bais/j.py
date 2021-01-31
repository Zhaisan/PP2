n = int(input())
a = list(map(int, input().split()))
D = 0
C = 0
for i in range(len(a)-1):
    if a[i]==1:
        D +=1
    elif a[i]==0 and a[i+1]==1:
        D +=1
    else:
        C +=1
if a[len(a)-1]==0:
    C +=1
else:
    D +=1
print("Clean:",end="")
print(C)
print("Dirty:",end="")
print(D)