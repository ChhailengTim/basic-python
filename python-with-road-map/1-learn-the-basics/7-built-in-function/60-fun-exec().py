from math import *

globalsParameter = {'__builtins__': None}
localsParameter = {'print': print, 'dir': dir}
exec('print(dir())', globalsParameter, localsParameter)
