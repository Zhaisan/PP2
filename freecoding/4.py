neededWeight = int(input())
realWeight = int(input())
if neededWeight > realWeight:
    print(neededWeight - realWeight)
elif realWeight > neededWeight:
    print(realWeight - neededWeight)
else:
    print("OK")