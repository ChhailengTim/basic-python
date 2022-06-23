# objects of this class are iterators
class PowTwo:
    def __init__(self, max):
        self.max = max

    def __iter__(self):
        self.num = 0
        return self

    def __next__(self):
        if self.num >= self.max:
            raise StopIteration
        result = 2 ** self.num
        self.num += 1
        return result


pow_two = PowTwo(5)
pow_two_iter = iter(pow_two)

print(list(pow_two_iter))