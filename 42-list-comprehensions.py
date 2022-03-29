a = [1, 3, 5, 7, 9, 11]
# [2,6,10,14,18,22]

b = []
b.append(10)
b.append(20)
print(b)

c = []
for x in a:
    c.append(x * 2)
    print(c)

d = [x * 2 for x in a]
print(d)
