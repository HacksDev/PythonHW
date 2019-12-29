import pickle

with open('marry.bak', 'rb') as f: marry = pickle.load(f)
marry.print_salary_info()