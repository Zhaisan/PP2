import re
text = str(input())
check = re.search('kbtu best|KBTU best|kbtubest|KBTUbest',text)
if(check == None):
    print('Not match!')
else:
    print('Found a match!')