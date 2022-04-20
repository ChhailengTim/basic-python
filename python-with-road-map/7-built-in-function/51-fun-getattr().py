class Student:
    marks = 88
    name = 'Sheeran'


person = Student()

name = getattr(person, 'name')
print(name)

marks = getattr(person, 'marks')
print(marks)

# Output: Sheeran
#         88
