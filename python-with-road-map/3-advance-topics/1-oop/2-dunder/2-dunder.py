# declare our own string class
class String:

    # magic method to initiate object
    def __init__(self, string):
        self.string = string

    # print our string object
    def __repr__(self):
        return 'Object: {}'.format(self.string)


# Driver Code
if __name__ == '__main__':
    # object creation
    string1 = String('Hello')

    # print object location
    print(string1)
