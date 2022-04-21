from math import *
exec('print(dir())', {'squareRoot': sqrt, 'pow': pow})

# object can have squareRoot() module
exec('print(squareRoot(9))', {'squareRoot': sqrt, 'pow': pow})