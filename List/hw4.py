inputResult = input("Введите символы (поддерживает отрицательные числа): \n")
numbers = [];
temp = ""
for ch in (inputResult+" "):
    sch = str(ch)
    if (sch in "0123456789"): temp += ch 
    elif (temp != "" and temp != "-"):
        numbers.append(int(temp))
        temp = ""
    else: temp = ""
    if (sch in "-"): temp = "-"
print(sum(numbers)) 