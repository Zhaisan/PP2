def exercise_10(s : set):
    set1 = set()
    for i in s :
        set1.add(i+1)
        set1.add(i-1)
    return(set1)
print(exercise_10({1, 5, 9}))
print(exercise_10({2, 5, 7, 8, 10}))
