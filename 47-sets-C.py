given_list = [1, 3, 4, 1, 3]

new_set = set()
for x in given_list:
    new_set.add(x)
total = 0
for x in new_set:
    total += x
    print(total)
