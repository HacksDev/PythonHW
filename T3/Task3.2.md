# Task3.2

## Task description

Написать функцию Фиббоначи fib(n), которая вычисляет элементы последовательности Фиббоначи:
```1 1 2 3 5 8 13 21 34 55 ...```

## Report

[File 3.2](Task3.2.py)   

```python
def fib(n):
    if (n == 0 or n == 1): return n
    return fib(n - 1) + fib(n - 2)
print(" ".join([str(fib(x)) for x in range(15)]))
```
