# Example 1
x = 5
print(callable(x))


def testFunction():
    print("Test")


y = testFunction
print(callable(y))


# Example 2
class Foo:
    def __call__(self):
        print('Print Something')


print(callable(Foo))


# Example 3
class Foo:
    def __call__(self):
        print('Print Something')


InstanceOfFoo = Foo()

# Prints 'Print Something'
InstanceOfFoo()


# Example 4.txt
class Foo:
    def printLine(self):
        print('Print Something')


print(callable(Foo))

InstanceOfFoo = Foo()
# Raises an Error
# 'Foo' object is not callable
InstanceOfFoo()
