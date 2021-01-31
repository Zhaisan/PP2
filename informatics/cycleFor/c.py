n = int(input())
for i in range(10**(n),10**(n-1)-1,-1):
    if i%2==1:
        print(i,end=' ')