l = list(map(int,input().split()))

def f(l):
    rev = []
    b = len(l)
    for i in range(-1, -b-1, -1):
        a = l[i]
        rev.append(a)
    return rev

print(f(l))