class stack:
    def __init__(self):
        self.stack = []

    def push(self, element):
        return self.stack.append(element)

    def __pos__(self):
        return self.stack.pop()

    def isEmpty(self):
        return len(self.stack) == 0

    def peek(self):
        if len(self.stack) != 0:
            return self.stack[-1]
        else:
            return "Stack is Empty"


create_stack = stack()
create_stack.push(5)
create_stack.push(2)
create_stack.push(3)
create_stack.push(4)

print(create_stack.stack)
# # `[5, 2, 3, 4]`
#
# # create_stack.pop()
# # `4`
#
# create_stack.peek()
# # `3`
#
# create_stack.pop()
# create_stack.pop()
# create_stack.pop()
# create_stack.isEmpty()
# # `True`
#
# create_stack.peek()
# 'Stack is Empty'
