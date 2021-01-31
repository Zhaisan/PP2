def ipis(x,y):
      if abs(x)<=1 and abs(y)<=0.5 or abs(y)<=1 and abs(x)<=0.5:
        return("YES")
      else:
        return("NO")
 
 
x1 = float(input())
x2 = float(input())
print(ipis(x1,x2))