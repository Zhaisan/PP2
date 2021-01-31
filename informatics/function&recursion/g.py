def power(a, n):
    if n == 0:
        return 1
    
    if a > 0:
        return a * power(a, n - 1)
 
print(power(int(input()), int(input())))