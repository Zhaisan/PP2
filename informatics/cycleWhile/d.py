k = int(input())
i = 0
while 2**i<=k:
    if 2 ** i == k:
        print("YES")
        exit()
    i +=1

print("NO")




    