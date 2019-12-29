# Task3.1

## Task description

Напишите функцию letters_range, которая ведет себя
похожим на range образом, однако в качестве start и
stop принимает не числа, а буквы латинского алфавита
(в качестве step принимает целое число) и возращает
не перечисление чисел, а список букв, начиная с
указанной в качестве start, до указанной в качестве
stop с шагом step (по умолчанию равным 1).

Пример:
```python
>>>letters_range('b', 'w', 2)
['b', 'd', 'f', 'h', 'j', 'l', 'n', 'p', 'r', 't', 'v']

>>>letters_range('a', 'g')
['a', 'b', 'c', 'd', 'e', 'f']

>>>letters_range('g', 'p')
['g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']

>>>letters_range('p', 'g', -2)
['p', 'n', 'l', 'j', 'h']

>>>letters_range('a','a')
[]
```

## Report

[File 3.1](Task3.1.py)   

```python
def letters_range(fr, to, step=1):
    return [chr(x) for x in range(ord(fr), ord(to), step)]
```
