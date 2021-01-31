import re
s=str(input())
a=str(input())
x=re.search(a,s)
print("First time "+a+" occured in position: ", x.start())
