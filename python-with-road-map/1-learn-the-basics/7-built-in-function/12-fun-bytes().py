# Example 1
string = "Python is interesting."

# string with encoding 'utf-8'
arr = bytes(string, 'utf-8')
print(arr)

# Example 2
size = 5

arr = bytes(size)
print(arr)

# Example 3
rList = [1, 2, 3, 4, 5]

arr = bytes(rList)
print(arr)