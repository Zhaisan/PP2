n = int(input())
if n == 0 or (n >= 5 and n <= 19) or (n%10==0) or (n % 5 == 0):
    print(n,"программистов")
elif (n % 10 == 6) or (n % 10 == 7) or (n % 10 == 8) or (n % 10 == 9):
    print(n,"программистов")
elif n // 100 >= 1:

        if (n // 10) % 10 == 1:
            
            print(n,"программистов")
elif n == 1 or (n % 10 == 1 and n != 11 and (n // 10) % 10 != 1):
    print(n,"программист")
elif (n >= 2 and n <= 4) or (n % 10 == 2 and (n // 10) % 10 != 1) or (n % 10 == 3 and (n // 10) % 10 != 1) or (n % 10 == 4 and (n // 10) % 10 != 1):
    print(n,"программиста")

