l = list(map(int,input().split()))
def f(l):
    even = [] 
    for i in range(0, len(l)): 
        if i % 2 == 0: 
            even.append(l[i])  
    return even
print(f(l))