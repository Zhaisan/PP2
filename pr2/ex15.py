def exercise_15(A,cnt):
    for i in range(len(A)):
        if i%2==0 and A[i]%2==1:
            cnt+=1
    return cnt

A = list(map(int, input().split()))
cnt = 0
print(exercise_15(A,cnt))