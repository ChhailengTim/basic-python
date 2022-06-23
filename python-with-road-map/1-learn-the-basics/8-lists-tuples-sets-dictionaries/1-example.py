l = []

l.append(5)
l.append(10)
print("Adding 5 and 10 in list", l)

l.pop()
print("Popped one element from list", l)
print()

s = set()

s.add(5)
s.add(10)
print("Adding 5 and 10 in set", s)

s.remove(5)
print("Removing 5 from set", s)
print()

t = tuple(l)

print("Tuple", t)
print()

d = {}

d[5] = "Five"
d[10] = "Ten"
print("Dictionary", d)

del d[10]
print("Dictionary", d)
