# Task1.6

## Task description
https://projecteuler.net/problem=36

The decimal number, 585 = 1001001001 in binary, is palindromic in both bases.
Find the sum of all numbers, less than one million, which are palindromic in
base 10 and base 2. (Please note that the palindromic number,
in either base, may not include leading zeros.)

Напишите программу, которая решает описанную выше задачу и печатает ответ.

## Report

[File 1.6](Task1.6.py)

```python
sum = 0
for i in range(1000000):
    base10 = str(i)
    if base10 != base10[::-1]: continue
    base2 = format(i, 'b')
    if base2 == base2[::-1]: sum += i
print(sum)

```