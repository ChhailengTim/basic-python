class My_class:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def instance_method(self):
        return f"This is the instance method and it can access the variables a={self.a} and \n b={self.b} with help of self."

obj=My_class(3,5)
obj.instance_method()
print(obj.instance_method())