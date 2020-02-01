## Report 6
```python
(sum([x for x in range(1,101)]))**2 - sum([x**2 for x in range(1,101)]) # 25164150
```

## Report 9
```python
[(x*y*(x**2 + y**2)**(0.5)) for x in range(400) for y in range(300) if (x+y+(x**2+y**2)**0.5 == 1000 and x != 0 and y != 0] # 31875000
```

## Report 48
```python
sum([x**x for x in range(1,1001)]) % 10000000000 # 9110846700
```

## Report 40
```python
from functools import reduce
reduce(lambda x, y: x * y,[int("".join([str(x) for x in range(10000001)])[10**z]) for z in range(7)]) #210 
```
