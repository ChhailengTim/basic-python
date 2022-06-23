class DoubleIt:

    def __init__(self):
        self.start = 1


def __iter__(self):
    return self

    def __next__(self):
        self.start *= 2
        return self.start

    __call__ = __next__


my_iter = iter(DoubleIt(), 16)

for x in my_iter:
    print(x)
