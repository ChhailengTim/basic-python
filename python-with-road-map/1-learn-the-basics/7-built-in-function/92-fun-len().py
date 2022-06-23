testString = ''
print('Length of', testString, 'is', len(testString))

testString = 'Python'
print('Length of', testString, 'is', len(testString))

# byte object
testByte = b'Python'
print('Length of', testByte, 'is', len(testByte))

testList = [1, 2, 3]

# converting to bytes object
testByte = bytes(testList)
print('Length of', testByte, 'is', len(testByte))