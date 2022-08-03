note1 = note2 = note5 = note10 = note20 = note50 = note100 = note500 = 0
amount = input("Enter amount: ")

if int(amount) >= 500:
    note500 = amount / 500;
    amount -= note500 * 500;
print("Total number of notes")
print("500 = ", note500)

