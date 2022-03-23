b = ["banana", "apple", "microsoft"]
print(b)

temp = b[0]
b[0] = b[2]
b[2] = temp
print(b)

b[0], b[2] = b[2], b[0]
print(b)
