class Foo:
    def __init__(self, a=5, b=10):
        self.a = a
        self.b = b


object = Foo()
print(vars(object))