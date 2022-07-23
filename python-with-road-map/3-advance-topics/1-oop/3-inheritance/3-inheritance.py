class MySuperClass1:

    def method_super1(self):
        print("method_super1 method called")


class MySuperClass2:

    def method_super2(self):
        print("method_super2 method called")


class ChildClass(MySuperClass1, MySuperClass2):

    def child_method(self):
        print("child method")


c = ChildClass()
c.method_super1()
c.method_super2()
