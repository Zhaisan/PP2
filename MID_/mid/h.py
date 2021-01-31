def  tri(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    elif n == 2:
        return 1


    return tri(n-3)+tri(n-2)+tri(n-1)

n = int(input())
print(tri(n))