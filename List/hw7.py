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
    if (users.setdefault(info[0], "") != ""): tempL.append(users.setdefault(info[0], "")) 
    for u in info[-1].split(','):
        if (users.setdefault(u, "") != ""): tempL.append(users.setdefault(u, "")) 
    groups[info[0]] = ", ".join(tempL)

print("-----------------------")
for g, c in groups.items(): print("Group: {:<20} -> Users UID: {:<20}".format(g, c))
