class Dog:
    attr1 = 'mammal'
    attr2 = 'cow'

    def fun(self):
        print("I am a", self.attr1)
        print("I am a", self.attr2)


Roger = Dog()
print(Roger.attr1)
Roger.fun()
