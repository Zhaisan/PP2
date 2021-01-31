a = int(input())
i = 2
cnt = 0
b =0
import math
while i<=math.sqrt(a)+1:
    if cnt!=1:
        if a%i==0:
            cnt+=1
            b = i
    i+=1   
if cnt!=1:
    print(a)
else:
    print(b)
        

    
    

    
    

        





