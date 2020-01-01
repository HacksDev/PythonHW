def fib(n):
    return n if (n == 0 or n == 1) else fib(n - 1) + fib(n - 2)
print(" ".join([str(fib(x)) for x in range(15)]))