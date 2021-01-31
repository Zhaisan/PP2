import re
s = str(input())
pattern = r'[A-Z]{1}[a-z]'
x = re.search(pattern,s)
if (x):
    print("Found a match!")
else:
    print("Not matched!") 

