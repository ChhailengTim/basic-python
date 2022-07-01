class My_class:
    def instance_method(self, a):
        return f"This is an instance method with a parameter a={a}."


obj = My_class()
obj.instance_method(10)
print(obj.instance_method(10))
