class Person:
    age = 23
    name = "Adam"


person = Person()
print('The age is:', getattr(person, "age"))
print('The age is:', person.age)
