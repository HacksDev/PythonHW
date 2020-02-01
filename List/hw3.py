words = {}
inputResult = list(input("Введите символы разделенные пробелом: \n").lower().split());
for elem in inputResult:
    words[elem] = words.setdefault(elem, 0) + 1
maximumValue = max(words.values())
for key in words.keys():
    if (words[key] == maximumValue): print("%s - %d" % (key, maximumValue))