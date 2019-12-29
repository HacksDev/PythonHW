def userInput():
    inp = input("Введите число: \n");
    if (inp.lower() == 'cancel'): return "Bye!"
    try: value = int(inp)
    except:
        print("Не удалось преобразовать введенный текст в число.")
        return userInput()
    return int(value / 2) if (value % 2 == 0) else value * 3 + 1
print(userInput())
