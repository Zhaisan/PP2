
def distance(x1,y1,x2,y2):
    c = (((x2-x1)**2)+((y2-y1)**2))**(1/2)
    return float(c)
a = float(input())
b = float(input())
c = float(input())
d = float(input())
print(distance(a,b,c,d))
