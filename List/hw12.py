def fib(n):
    return n if (n == 0 or n == 1) else fib(n - 1) + fib(n - 2)

def fib_incremental(n, n0 = 0, n1 = 1):
    return n0 if n == 0 else n1 if (n == 1) else fib_incremental(n - 1, n1, n0 + n1)

def fib_while(n):
    n0 = 1
    n1 = 1
    result = [str(n0), str(n1)]
    i = 2
    while i < n:
        sum = n0 + n1
        n0 = n1
        n1 = sum
        result.append(str(sum))
        i += 1
    return result

def fib_list(n):
    fl = [1, 1]
    for i in range(2, n):
        fl.append(fl[i-2] + fl[i-1])
    return fl

print(" ".join([str(fib(x)) for x in range(1, 16)]))
print(" ".join([str(fib_incremental(x)) for x in range(1, 16)]))
print(" ".join(fib_while(15)))
print(" ".join(str(x) for x in fib_list(15)))