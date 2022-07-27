class Person:
    def __init__(self, name):
        self.name = name

    def say_hi(self):
        print("Hello, my name is ", self.name)


p = Person("Kim")
print(p.name)
p.say_hi()
