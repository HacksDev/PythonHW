# Task2.1

## Task description

Напишите программу, которая читает данные из файлов
/etc/passwd и /etc/group на вашей системе и выводит
следующую информацию в файл output.txt:
1. Количество пользователей, использующих все имеющиеся
интерпретаторы-оболочки.
```( /bin/bash - 8 ; /bin/false - 11 ; ... )```
2. Для всех групп в системе - UIDы пользователей
состоящих в этих группах.
```( root:1, sudo:1001,1002,1003, ...)```

## Report

[Passwd](passwd)    
[Group](group)    
[Execution Result](Result.txt)    

[File 2.1](Task2.1.py)   

```python
f = open('/etc/passwd', 'r')
stringsList = f.readlines()
counterDict = {}
users = {}
for line in stringsList:
    info = line.strip().split(':')
    counterDict[info[-1]] = counterDict.setdefault(info[-1], 0) + 1
    users[info[0]] = info[2]
f.close()

for u, c in counterDict.items(): print("Shell: {:<20} -> Count: {:<20}".format(u, c))

f = open('/etc/group','r')
groupsList = f.readlines()
groups = {}
for line in groupsList:
    info = line.strip().split(':')
    tempL = []
    for u in info[-1].split(','):
        tempL.append(users.setdefault(u, "-"))
    groups[info[0]] = ", ".join(tempL)
print("-----------------------")
for g, c in groups.items(): print("Group: {:<20} -> Users UID: {:<20}".format(g, c))
```
