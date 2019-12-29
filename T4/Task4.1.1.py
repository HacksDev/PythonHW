import pickle
from Employee import Employee

marry = Employee("Marry", "+126446", salary=5000)
with open('marry.bak', 'wb+') as f: pickle.dump(marry, f)
del marry