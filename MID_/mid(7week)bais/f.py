n = int(input())
s = str(input())
for i in range(len(s)):
    if ord(s[i])+n>90:
        print(chr(ord(s[i])+n-26),end="")
    else:
        print(chr(ord(s[i])+n),end="")


    