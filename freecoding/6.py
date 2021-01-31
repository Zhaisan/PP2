word = str(input())
letter = input()
for i in range(len(word)):
    if letter == word[i]:
        print("YES")
        exit()

print("NO")