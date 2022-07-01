from datetime import date


class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def Year(cls, name, year):
        return cls(name, date.today().year - year)


Dog1 = Dog('Bruno', 1)
Dog1.name, Dog1.age
print(Dog1.name)
print(Dog1.age)


Dog2 = Dog('Bobby', 2020)
Dog2.name, Dog2.age
print(Dog2.name)
print(Dog2.age)