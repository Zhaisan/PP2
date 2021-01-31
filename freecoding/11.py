a = int(input())
b = int(input())
c = int(input())
if a < (b+c) and b < (a+c) and c < (a+b):
    if a!=b and a!=c and b!=c:
        print("Разносторонний")
    if a==b and a!=c and b!=c:
        print("Равнобедренный")
    if a==b and a==c and b == c:
        print("Равносторонний")
else:
    print("NO")