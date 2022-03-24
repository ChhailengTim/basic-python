print(list(range(1, 8)))
total = 0
for i in range(1, 8):
    if i % 3 == 0:
        total += i
    print(total)
