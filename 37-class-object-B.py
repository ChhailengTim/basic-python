class Person:
    def __init__(self, n, p, i):
        self.name = n
        self.personality = p
        self.is_sitting = i

    def sit_down(self):
        self.is_sitting = True

    def stand_up(self):
        self.is_sitting = False


p1 = Person("Alice", "Aggressive", False)
p2 = Person("Tommy", "Talkative", True)

# p1 owns r2

# p1.robot_owned = r2
# p2.robot_owned = r1
