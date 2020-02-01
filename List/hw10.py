def collatz(n, c=0):
    print(int(n))
    if (n == 1): return "Всего шагов: {}".format(c)
    return collatz(n/2, c + 1) if (n % 2 == 0) else collatz(3*n + 1, c + 1)
print(collatz(27))

