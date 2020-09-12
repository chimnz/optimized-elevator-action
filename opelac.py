import numpy as np
from sys import argv

CALLS_FILE = argv[1]  # path to input file => {time} {floor} {dest} on each line
dtype = [('time', 'f'), ('floor', 'i'), ('dest', 'i')]  # "f" is for float, "i" is for integer
calls = np.loadtxt(fname=CALLS_FILE, dtype=dtype)  # [(time1, floor1, dest1), (time2, floor2, dest2), ...]
calls = sorted(calls, key=lambda x: x[0])  # sort calls by time
print(calls)