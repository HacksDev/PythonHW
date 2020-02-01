sum = 0
for i in range(1000000):
    base10 = str(i)
    if base10 != base10[::-1]: continue
    base2 = format(i, 'b')
    if base2 == base2[::-1]: sum += i
print(sum)