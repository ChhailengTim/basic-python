from math import *

print(eval('dir()', {'sqrt': sqrt, 'pow': pow}))


names = {'square_root': sqrt, 'power': pow}
print(eval('dir()', names))

# Using square_root in Expression
print(eval('square_root(9)', names))
