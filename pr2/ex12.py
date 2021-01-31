def exercise_12(my_list: list):
    some_set = set()

    for i in my_list:
        temp = i
        while temp in some_set:
            temp*=i
        some_set.add(temp)
    return some_set

print(exercise_12([1, 2, 2]))
print(exercise_12([1, 2, 2, 3, 4]))