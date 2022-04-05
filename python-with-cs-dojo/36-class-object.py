class Robot:
    def __init__(self, name, color, weight):
        self.name = name
        self.color = color
        self.weight = weight

    def introduce_self(self):
        print("My name is " + self.name)  # this in java


# r1 = Robot()
# r1.name = "Tom"
# r1.color = "Red"
# r1.weight = 30
# r1.introduce_self()
#
# r2 = Robot()
# r2.name = "Jerry"
# r2.color = "blue"
# r2.weight = 30
# r2.introduce_self()

r1 = Robot("Tom", "Red", 30)
r1.introduce_self()

r2 = Robot("Jerry", "Blue", 30)
r2.introduce_self()
