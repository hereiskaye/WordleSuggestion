import random 
import numpy as np

import json


a = np.random.rand(5000,8)

np.save('testing.npy', a)

b = np.load('testing.npy')

print(a==b)

with open('testing.txt', 'w') as filehandle:
  json.dump(a.tolist(), filehandle)
