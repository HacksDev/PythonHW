# Task1.5

## Task description
Встроенная функция input позволяет ожидать и возвращать данные из стандартного
ввода ввиде строки (весь введенный пользователем текст до нажатия им enter).
Используя данную функцию, напишите программу, которая:

1. После запуска предлагает пользователю ввести неотрицательные целые числа,
разделенные через пробел и ожидает ввода от пользователя.
2. Находит наименьшее положительное число, не входящее в данный пользователем
список чисел и печатает его.


Например:
```
-> 2 1 8 4 2 3 5 7 10 18 82 2
6
```

## Report

[File 1.5](Task1.5.py)

Solution with sets
```python
numbers = list(map(int,input("Введите числа через пробел: \n").split()))
maximum, minimum = max(numbers) + 2, min(numbers)
diff = list(set([k for k in range(minimum, maximum, 1)]) - set(numbers))
if (diff): print(min(diff))
```

Solution with range
```python
numbers = list(map(int,input("Введите числа через пробел: \n").split()))
for i in range(min(numbers), max(numbers) + 2): 
    if (not i in numbers): 
        print(i)
        break
```