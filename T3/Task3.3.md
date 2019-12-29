# Task3.3

## Task description

Напишите функцию, которая переводит значения показаний
температуры из Цельсия в Фаренгейт и наоборот.

## Report

[File 3.3](Task3.3.py)   

```python
def CtoF(degree, direct_order=True):
    return (degree * 9/5 + 32) if (direct_order) else ((degree - 32) * 5/9)
```
