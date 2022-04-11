class Person:
    def __dir__(self):
        return ['age', 'name', 'salary']


teacher = Person()
print(dir(teacher))
