given_list = [7, 5, 4, 4, 3, 1, -2, -3, -5, -7]
total = 0
i = 0
while True:
    total += given_list[i]
    i += 1
    if given_list[i] <= 0:
        break
print(total)

