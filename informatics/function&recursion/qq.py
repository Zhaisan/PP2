def modify_list(l):
    # put your python code here
    l = []
    for i in range(len(l)):
        if l[i] % 2 == 1:
            l.remove(l[i])
            continue
            l[i] /= 2
    return l
s = int(input())
print(modify_list(s))