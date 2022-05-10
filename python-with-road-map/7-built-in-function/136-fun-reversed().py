class Vowels:
    vowels = ['a', 'e', 'i', 'o', 'u']

    def __reversed__(self):
        return reversed(self.vowels)


v = Vowels()
print(list(reversed(v)))
