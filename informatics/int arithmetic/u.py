x = int(input())
k = int(input())
cnt = 1
cnt1  = 1
n = k//x
cnt1 = cnt + n
if (k/x)==(n/cnt):
    print(cnt1-1)
if (k/x)>(n/cnt):
    print(cnt1)
if (k/x)<(n/cnt):
    print(cnt1)