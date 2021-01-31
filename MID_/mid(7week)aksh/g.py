import re
txt = str(input())
p = str(input())
q = str(input())
gang = str(input())
res1 = re.sub(p,q,txt)
res2 = re.findall(gang,res1)
print(len(res2))