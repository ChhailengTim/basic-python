from decimal import Decimal

# normal float
num = 2.675
print(round(num, 2))

# using decimal.Decimal (passed float as string for precision)
num = Decimal('2.675')
print(round(num, 2))
