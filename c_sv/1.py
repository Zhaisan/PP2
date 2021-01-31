import csv

with open("1.txt", "r",encoding='utf-8') as f:
    lines = f.readlines()

students = []
title = ["#", "id", "Name", "Surname", "MName", "Spec"]
students.append(title)

# row = 2

for row in range(0, len(lines) // 4):
    line1 = lines[row * 4]
    line2 = lines[row * 4 + 1]
    line3 = lines[row * 4 + 2]
    line4 = lines[row * 4 + 3]
    try:
        name, surname, mname = line3.split()
    except:
        name, surname = line3.split()
        mname = ''
    line = [line1, line2, name, surname, mname, line4]
    students.append(line)

with open("3.csv", "w",encoding='utf-8') as f:
    writer = csv.writer(f, delimiter = ';',lineterminator = '\n')
    writer.writerows(students)