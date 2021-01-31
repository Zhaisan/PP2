Q = input()
x = int(input())
y = int(input())
x1 = 0
y1 = 0
ans  = False
for i in range(len(Q)):
    if Q[i]=="R":
        x1 +=1
    elif Q[i]=="L":
        x1 -=1
    elif Q[i]=="U":
        y1 +=1
    elif Q[i]=="D":
        y1 -=1
    if x1==x and y1==y:
        ans = True
if ans ==True:
    print("Passed")
else:
    print("Missed")
    
