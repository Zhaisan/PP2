def bigger(a, n):
    b = []
    for pos in range(len(a)):
        if a[pos] > n :
            b.append(a[pos])
    print(b) 
a = int(input())
alist = [int(input()) for i in range(a)] 
n = int(input())
bigger(alist, n)