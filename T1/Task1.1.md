# Task1.1

## Task description
1. Составить таблицу соответствия между различными объектами основных классов: int, str и объектами класса bool.
2. Разобраться с различиями между ```input()``` и ```raw_input()```. Также в контексте разных версий python: 2 и 3.
3. Найти и прочитать PEP про изменение print между python2 и python3.

## Report

### 1. Таблица соответствий

По умолчанию объект считается истинным, если его класс не определяет метод ```__bool__ ()```, возвращающий значение ```False```, или метод ```__len__ ()```, возвращающий ноль при вызове объекта. [Docs](https://docs.python.org/3/library/stdtypes.html)

| Тип | Значение | Bool
| :--- | :---: | :--- 
| int | 0 | False
| int | 1 | True
| int | -1 | True
| float | 0.0 | False
| float | 0.1 | True
| complex | 0j | False
| complex | 1j | True
| Decimal| Decimal(0) | False
| Decimal| Decimal(1) | True
| Str | '' | False
| Str | 'a' | True
| Str | '\0' | True
| Tuple | () | False
| Tuple | (a) | True
| List | [] | False
| List | [1] | True
| Dict | {} | False
| Dict | {1} | True
| Set | set() | False
| Set | set('123') | True
| Range | range() | False
| Range | range(1) | True

### 2. Различия input() и raw_input()

#### Python 2:

**raw_input([prompt])**

Если аргумент ```prompt``` присутствует, то он выводится без символов переноса строки. Затем функция считывает строку из входных данных и преобразует ее в строку (удаляя перенос строки) и возвращает ее. При чтении EOF возникает ошибка EOFError.

**input()**
В отличие от предыдущей функции, пытается произвести выполнение того, что вводит пользователь.

Эквивалент ```python2 eval(raw_input(prompt))```.

Если входные данные не являются синтаксически допустимыми, будет вызвана ```SyntaxError```. Другие исключения могут возникать, если во время выполнения (```eval()```) возникает ошибка.

#### Python 3:

**raw_input([prompt])**

Отсутствует

**input()**

Выполняет роль ```raw_input()``` в Python2.

### 3. Различия в print между 2 и 3 версией Python

[PEP 3105](https://www.python.org/dev/peps/pep-3105/)

**Обоснование**

- Не рационально выделять отдельную *языковую синтаксическую* конструкцию на те нужды, которые можно решить функционально на уровне модуля языка.
- Синтаксическая природа конструкции создает дополнительные барьеры для расширения функций со схожим функционалом ```printf()``` .
- Отсутствует возможность задания дополнительных параметров, например символов-склейки при выводе.
- Если ```print()``` функция, то существует возможность переопределить ее поведение. 
- Не функциональная синтаксическая конструкцая затрудняет передачу ее в качестве параметра функции. 
