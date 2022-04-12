from math import *

a = 169
print(eval('sqrt(a)', {'__builtins__': None}, {'a': a, 'sqrt': sqrt}))