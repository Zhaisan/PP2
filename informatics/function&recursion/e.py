
def ipic(x, y, xc, yc, r):
    if r >= (((x-xc)**2) + ((y - yc)**2))**(1/2):
        return("YES")
    else :
        return("NO")
a = float(input())
b = float(input())
c = float(input())
d = float(input())
q = float(input())
print(ipic(a,b,c,d,q))
    
