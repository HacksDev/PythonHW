# Task5.1

## Task description

Написать программу, которая будет считывать из файла gps координаты,
и формировать текстовое описание объекта и ссылку на google maps.
Пример:

```
Input data: 60,01';30,19'
Output data:
Location: Теремок, Енотаевская улица, Удельная, округ Светлановское, Выборгский район, Санкт-Петербург, Северо-Западный федеральный округ, 194017, РФ
Goggle Maps URL: https://www.google.com/maps/search/?api=1&query=60.016666666666666,30.322
```

## Report

Требует обязательного использования ключа API, который становится активным для конкретного сервиса после указания платежных реквезитов. Ранее использовалась библиотека ```geocoder``` или ```pygeocoder``` 

Сервис Google Maps был заменен на OpenCage
[Датасет: https://developers.google.com/public-data/docs/canonical/countries_csv](https://developers.google.com/public-data/docs/canonical/countries_csv)    

Preparing
```python
pip install geocoder
```

[File 5.1](Task5.1.py)

```python
import geocoder
import os
API_KEY = "0cd871cf1c01475ea28e5b0e4ac32a37"

lines = []
with open(os.path.dirname(os.path.abspath(__file__))+'\coords.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    x, y = line.split('	')[1], line.split('	')[2] 
    print("Input coords: {:>10}, {:>10}".format(x, y))
    location = geocoder.opencage([x, y], method='reverse', key=API_KEY).json['address']
    print("Location:", location)
    print("GoogleMaps URL:", "https://www.google.com/maps/search/?api=1&query={},{}".format(x,y))
    print()
```