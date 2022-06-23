class Coordinate:
  x = 10
  y = -5
  z = 0

point1 = Coordinate()

print('x = ',point1.x)
print('y = ',point1.y)
print('z = ',point1.z)

# Deleting attribute z
del Coordinate.z

print('--After deleting z attribute--')
print('x = ',point1.x)
print('y = ',point1.y)

# Raises Attribute Error
print('z = ',point1.z)