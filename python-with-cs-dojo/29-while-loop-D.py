given_list = [5, 4, 4, 3, 1, -2, -3, -5]
total = 0
for element in given_list:
    if element <= 0:
        break
    total += element
    print(total)
