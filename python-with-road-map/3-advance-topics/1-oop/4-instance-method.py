class My_class:
    def instance_method(self):
        print("Hello! from %s" % self.__class__.__name__)

obj=My_class()
obj.instance_method()
print(obj.instance_method())