n,x = map(int, input().split())
q = [int(i) for i in input().split()]
ans = False
for i in range(n):
    for j in range(i+1,n):
        if q[i]+q[j] == x:
            ans = True

            
            
if ans == True:
    print("Bon Appetit")
else:
    print("So sad")





