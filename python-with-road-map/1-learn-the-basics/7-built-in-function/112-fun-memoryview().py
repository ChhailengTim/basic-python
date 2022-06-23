# random bytearray
random_byte_array = bytearray('ABC', 'utf-8')

mv = memoryview(random_byte_array)

# access memory view's zeroth index
print(mv[0])

# create byte from memory view
print(bytes(mv[0:2]))

# create list from memory view
print(list(mv[0:3]))
