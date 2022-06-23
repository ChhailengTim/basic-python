class PrintNumber:
    def __init__(self, max):
        self.max = max

    def __iter__(self):
        self.num = 0
        return self

    def __next__(self):
        if self.num >= self.max:
            raise StopIteration
        self.num += 1
        return self.num


# print_num is an iterable
print_num = PrintNumber(5)

# creating a set
print(set(print_num))
