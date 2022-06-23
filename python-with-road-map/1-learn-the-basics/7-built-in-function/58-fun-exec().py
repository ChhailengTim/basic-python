from math import *
exec('print(dir())', {'sqrt': sqrt, 'pow': pow})

# object can have sqrt() module
exec('print(sqrt(9))', {'sqrt': sqrt, 'pow': pow})