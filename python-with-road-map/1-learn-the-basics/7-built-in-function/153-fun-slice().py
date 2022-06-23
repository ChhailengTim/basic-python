py_list = ['P', 'y', 't', 'h', 'o', 'n']
py_tuple = ('P', 'y', 't', 'h', 'o', 'n')

# contains indices -1, -2 and -3
slice_object = slice(-1, -4, -1)
print(py_list[slice_object])  # ['n', 'o', 'h']

# contains indices -1 and -3
slice_object = slice(-1, -5, -2)
print(py_tuple[slice_object]) # ('n', 'h')