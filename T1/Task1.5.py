# Solution 1
numbers = list(map(int,input("Введите числа через пробел: \n").split()))
maximum, minimum = max(numbers) + 2, min(numbers)
diff = list(set([k for k in range(minimum, maximum, 1)]) - set(numbers))
if (diff): print(min(diff))

# Solution 2
numbers = list(map(int,input("Введите числа через пробел: \n").split()))
for i in range(min(numbers), max(numbers) + 2): 
    if (not i in numbers): 
        print(i)
        break