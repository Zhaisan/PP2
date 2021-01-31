throwBolat1 = int(input())
throwBolat2 = int(input())
throwAlina1 = int(input())
throwAlina2 = int(input())
a = throwBolat1 + throwBolat2
b = throwAlina1 + throwAlina2
if a > b :
    print("BOLAT")
elif a < b:
    print("ALINA")
else:
    print("DRAW")