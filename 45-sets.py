# sets in Python
# A set is a type of data that stores a set of things.
# A set of unique things.
# {1, 3} <- 3
# -> {1, 3}
a = set()
print(a)
a.add(1)
print(a)
a.add(2)
print(a)
a.add(2)
print(a)

for x in a:
    print(x)
    