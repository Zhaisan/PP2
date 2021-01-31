import re
txt = str(input())
if re.search("\W",txt):
    print("Not matched!")
else:
    print("Found a match!")