
# custom __format__() method
class Person:
    def __format__(self, format):
        if(format == 'age'):
            return '23'
        return 'None'

print(format(Person(), "age"))